from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from routers.tariff import tariff_entry
from routers.ai import ai_entry
from routers.history import history_entry
from utils.menu import show_full_menu, show_welcome_menu
from utils.chekers import delete_menu_if_not_in_prompt

start_router = Router(name="start")


@start_router.message(F.text == "/start")
async def on_start(msg: Message, state: FSMContext) -> None:
    await show_full_menu(msg, state)


@start_router.message(F.text == "🏠 Новая задача")
async def on_new_task(msg: Message, state: FSMContext):
    await delete_menu_if_not_in_prompt(msg, state)
    await show_welcome_menu(msg, state)


@start_router.message(F.text == "💾 История задач")
async def on_history(msg: Message, state: FSMContext):
    await delete_menu_if_not_in_prompt(msg, state)
    await history_entry(msg, state)


@start_router.message(F.text == "💳 Тарифы")
async def on_tariff(msg: Message, state: FSMContext):
    await delete_menu_if_not_in_prompt(msg, state)
    await tariff_entry(msg)


@start_router.callback_query(F.data == "choose_ai")
async def choose_ai_cb(cb, state):
    await cb.answer()
    await cb.message.edit_reply_markup(reply_markup=None)
    await cb.message.delete()
    await ai_entry(cb.message, state)
