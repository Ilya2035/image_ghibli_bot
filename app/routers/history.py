from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from states import Flow
from utils.menu import show_welcome_menu
from routers.ai import choose_prompt as ai_choose_prompt

history_router = Router(name="history")

kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧠 Повторить последний запрос", callback_data="pr:ads")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="history:back")],
    ])


@history_router.message(F.text == "💾 История задач")
async def history_entry(msg: Message, state: FSMContext):

    await msg.answer(
        "Здесь пока будет история ваших запросов:",
        reply_markup=kb,
    )


@history_router.callback_query(F.data.startswith("pr:"))
async def history_repeat(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.update_data(
        mode="single",
        ai="text",
        cat="copy",
        prompt="ads"
    )
    await ai_choose_prompt(cb, state)


@history_router.callback_query(F.data == "history:back")
async def history_back(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await cb.message.delete()
    await show_welcome_menu(cb.message, state)
