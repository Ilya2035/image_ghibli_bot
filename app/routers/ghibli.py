from __future__ import annotations

import io
import tempfile

from aiogram import F, Router
from aiogram.types import BufferedInputFile, Message
from aiogram.utils.chat_action import ChatActionSender

from crud.request_transactions import add_photo_request
from crud.save_transactions import save_output_to_db
from crud.user_transactions import add_user
from db.session import async_session
from utils.image_generation import replicate_image

photo_router = Router()


@photo_router.message(F.photo)
async def handle_photo(message: Message) -> None:
    bot = message.bot
    tg_id = str(message.from_user.id)
    photo = message.photo[-1]

    tg_file = await bot.get_file(photo.file_id)
    buffer = io.BytesIO()
    await bot.download_file(tg_file.file_path, destination=buffer)

    buffer.seek(0)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        temp_file.write(buffer.read())
        temp_file_path = temp_file.name

    async with async_session() as session:
        user = await add_user(session, tg_id)
        req = await add_photo_request(
            session,
            user_id=user.id,
            photo_bytes=buffer.getvalue(),
        )
        await session.commit()

    await message.answer(
        "Фото загружено ✅\n"
        "Рисую версию в стиле Ghibli, подождите…"
    )

    async with ChatActionSender.typing(message.chat.id, message.bot):
        # Теперь передаем temp_file как открытый файл
        with open(temp_file_path, "rb") as file_to_send:
            anime_bytes = await replicate_image(file_to_send)

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
