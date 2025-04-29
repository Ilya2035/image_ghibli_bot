from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.main_keyboards import kb_start, kb_global
from promt.start_promt import WELCOME_TEXT
from routers.tariff import tariff_entry
from routers.ai import ai_entry


start_router = Router(name="start")


@start_router.message(F.text.in_({"/start", "🏠 Меню"}))
async def cmd_start(msg: Message, state: FSMContext) -> None:
    await state.clear()

    await msg.answer("\u2063", reply_markup=kb_global())
    await msg.answer(WELCOME_TEXT, reply_markup=kb_start())


@start_router.message(F.text == "💳 Тарифы")
async def go_tariff(msg: Message) -> None:
    await tariff_entry(msg)


@start_router.callback_query(F.data == "choose_ai")
async def choose_ai_cb(cb, state):
    await cb.answer()
    await cb.message.edit_reply_markup(reply_markup=None)
    await ai_entry(cb.message, state)
