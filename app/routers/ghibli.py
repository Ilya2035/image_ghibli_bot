from __future__ import annotations

import io
from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile

from db.session import async_session
from crud.user_transactions import add_user
from crud.request_transactions import add_photo_request
from crud.stylize_transactions import stylize_from_db
from crud.save_transactions import save_output_to_db

photo_router = Router()


@photo_router.message(F.photo)
async def handle_photo(message: Message) -> None:
    """
    1. скачиваем фото (bytes)
    2. создаём / берём пользователя
    3. пишем запрос в БД (status='processing')
    4. шлём «ждите…»
    5. вызываем OpenAI → получаем результат
    6. сохраняем результат (status='done' / 'error')
    7. отправляем картинку или сообщение об ошибке
    """
    bot = message.bot
    tg_id = str(message.from_user.id)
    photo = message.photo[-1]

    tg_file = await bot.get_file(photo.file_id)
    buf = io.BytesIO()
    await bot.download_file(tg_file.file_path, destination=buf)
    raw_bytes = buf.getvalue()

    async with async_session() as session:
        user = await add_user(session, tg_id)
        req = await add_photo_request(
            session,
            user_id=user.user_id,
            photo_bytes=raw_bytes,
        )

    await message.answer(
        "Фото загружено ✅\n"
        "Рисую в стиле Ghibli, пожалуйста подождите…"
    )

    async with async_session() as session:
        result_bytes = await stylize_from_db(session, req.id)
        await save_output_to_db(session, req.id, result_bytes)

    if result_bytes:
        await message.answer_photo(
            BufferedInputFile(result_bytes, filename="ghibli.png"),  # ✔
            caption="Готово! 🎨"
        )
    else:
        await message.answer("Не удалось обработать изображение 😔")
