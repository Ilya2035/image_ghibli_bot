from __future__ import annotations

import io

from aiogram import F, Router
from aiogram.types import BufferedInputFile, Message
from aiogram.utils.chat_action import ChatActionSender

from crud.request_transactions import add_photo_request
from crud.save_transactions import save_output_to_db
from crud.user_transactions import add_user
from db.session import async_session
from utils.image_generation import ghibli_style_transfer

photo_router = Router()


@photo_router.message(F.photo)
async def handle_photo(message: Message) -> None:
    """
    Полный цикл обработки фото:
    1. скачиваем из Telegram;
    2. фиксируем пользователя + Request(status='processing');
    3. сообщаем пользователю о начале работы;
    4. отправляем изображение в Replicate;
    5. сохраняем результат;
    6. отвечаем пользователю.
    """
    bot = message.bot
    tg_id = str(message.from_user.id)
    photo = message.photo[-1]

    tg_file = await bot.get_file(photo.file_id)
    buffer = io.BytesIO()
    await bot.download_file(tg_file.file_path, destination=buffer)
    jpeg_bytes = buffer.getvalue()

    async with async_session() as session:
        user = await add_user(session, tg_id)
        req = await add_photo_request(
            session,
            user_id=user.id,
            photo_bytes=jpeg_bytes,
        )
        await session.commit()

    await message.answer(
        "Фото загружено ✅\n"
        "Рисую версию в стиле Ghibli, подождите…"
    )

    async with ChatActionSender.typing(message.chat.id, message.bot):
        anime_bytes = await ghibli_style_transfer(jpeg_bytes)

    async with async_session() as session:
        await save_output_to_db(session, req.id, anime_bytes)
        await session.commit()

    if anime_bytes:
        preview = BufferedInputFile(anime_bytes, filename="ghibli_preview.jpg")
        original = BufferedInputFile(anime_bytes, filename="ghibli_full.png")

        await message.answer_photo(preview, caption="Готово! 🎨 (превью)")
        await message.answer_document(original, caption="Ваш файл")
    else:
        await message.answer("Не удалось преобразовать изображение 😔")
