from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from routers.tariff import tariff_entry
from routers.ai import ai_entry
from routers.history import history_entry
from utils.menu import show_full_menu, show_welcome_menu
from utils.chekers import delete_menu_if_not_in_prompt
from keyboards.main_keyboards import kb_choice_task, kb_choice_history

start_router = Router(name="start")


@start_router.message(F.text == "/start")
async def on_start(msg: Message, state: FSMContext) -> None:
    await show_full_menu(msg, state)


@start_router.message(F.text == "🏠 Новая задача")
async def on_new_task(msg: Message, state: FSMContext):
    await delete_menu_if_not_in_prompt(msg, state)

    await msg.answer(
        "Вы уверены, что хотите начать новую задачу?\n"
        "Текущий диалог будет сохранён в истории.",
        reply_markup=kb_choice_task()
    )


@start_router.callback_query(F.data == "new_task:yes")
async def new_task_confirm(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await cb.message.delete()
    await show_welcome_menu(cb.message, state)


@start_router.callback_query(F.data == "new_task:no")
async def new_task_cancel(cb: CallbackQuery, state: FSMContext):
    await cb.answer(text="Отмена", show_alert=True)
    await cb.message.delete()


@start_router.message(F.text == "💾 История задач")
async def on_history(msg: Message, state: FSMContext):
    await delete_menu_if_not_in_prompt(msg, state)

    await msg.answer(
        "Хотите прервать текущий диалог и перейти к истории?\n"
        "Текущий запрос будет сохранён.",
        reply_markup=kb_choice_history()
    )


@start_router.callback_query(F.data == "history:yes")
async def history_confirm(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await cb.message.delete()
    await history_entry(cb.message, state)


@start_router.callback_query(F.data == "history:no")
async def history_cancel(cb: CallbackQuery, state: FSMContext):
    await cb.answer(text="Отмена", show_alert=True)
    await cb.message.delete()


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
