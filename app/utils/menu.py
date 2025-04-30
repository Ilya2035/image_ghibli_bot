from pathlib import Path
from aiogram.types import Message, BufferedInputFile, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from db.session import async_session
from crud.user_transactions import add_user
from keyboards.main_keyboards import kb_global, kb_start
from prompt.start_promt import WELCOME_TEXT


async def show_full_menu(msg: Message, state: FSMContext):
    """
    Используется при /start:
      1) показываем картинку (если есть)
      2) ставим глобальную клавиатуру
      3) отправляем приветственный текст + inline-кнопки
    """
    await state.clear()
    async with async_session() as session:
        await add_user(session, str(msg.from_user.id))
        await session.commit()

    path = Path("data/main_foto/mainfoto.png")
    if path.exists():
        with path.open("rb") as f:
            photo = BufferedInputFile(f.read(), filename="mainfoto.png")
        await msg.answer_photo(photo, reply_markup=kb_global())
    else:
        # если картинки нет, всё равно показываем глобальную клавиатуру
        await msg.answer("\u2063", reply_markup=kb_global())

    await msg.answer(WELCOME_TEXT, reply_markup=kb_start())


async def show_welcome_menu(msg: Message, state: FSMContext):
    """
    Используется при «🏠 Новая задача»:
      • Убираем старую reply-клавиатуру (она уже осталась после предыдущих шагов)
      • Сразу шлём только приветственный текст + inline-кнопки
    """
    await state.clear()
    await msg.answer(WELCOME_TEXT, reply_markup=kb_start())
