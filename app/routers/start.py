from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет, это бот, который нарисует твою картинку в другом стиле.\n\n"
        "Стиль называется 'Ghibli'. Всё, что нужно сделать — это \n"
        "отправить фото и подождать, пока бот пришлёт новую!"
    )
