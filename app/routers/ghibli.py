from __future__ import annotations

import io
from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile

from db.session import async_session
from crud.user_transactions import add_user
from crud.request_transactions import add_photo_request
from crud.save_transactions import save_output_to_db
from utils.image_generation import replicate_anime

photo_router = Router()


@photo_router.message(F.photo)
async def handle_photo(message: Message) -> None:
    """
    1. скачиваем фото (bytes)
    2. фиксируем пользователя и создаём Request(status='processing')
    3. шлём 'ждите…'
    4. отправляем фото на Replicate → получаем anime-bytes
    5. обновляем Request (status='done'/'error')
    6. отправляем пользователю результат или ошибку
    """
    bot = message.bot
    tg_id = str(message.from_user.id)
    photo = message.photo[-1]

    # 1. скачать фото из Telegram
    tg_file = await bot.get_file(photo.file_id)
    buf = io.BytesIO()
    await bot.download_file(tg_file.file_path, destination=buf)
    jpeg_bytes = buf.getvalue()

    # 2. пользователь + запись запроса
    async with async_session() as session:
        user = await add_user(session, tg_id)
        req = await add_photo_request(
            session,
            user_id=user.user_id,
            photo_bytes=jpeg_bytes,
        )

    # 3. сообщение пользователю
    await message.answer(
        "Фото загружено ✅\n"
        "Рисую аниме-версию в стиле Ghibli, подождите…"
    )

    # 4. запрос к Replicate
    anime_bytes = await replicate_anime(jpeg_bytes)

    # 5. обновляем запись
    async with async_session() as session:
        await save_output_to_db(session, req.id, anime_bytes)

    # 6. ответ
    if anime_bytes:
        await message.answer_photo(
            BufferedInputFile(anime_bytes, filename="ghibli.png"),
            caption="Готово! 🎨"
        )
    else:
        await message.answer("Не удалось преобразовать изображение 😔")
