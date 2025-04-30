from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import Flow
from keyboards.ai_keyboards import kb_mode, kb_ai_types, kb_categories, kb_prompts


async def show_mode(msg: Message, state: FSMContext):
    await state.set_state(Flow.choose_mode)
    await msg.answer("Шаг 1/4 — Выберите режим работы:", reply_markup=kb_mode())


async def show_ai(msg: Message, state: FSMContext):
    await state.set_state(Flow.choose_ai)
    await msg.answer("Шаг 2/4 — выберите тип ИИ:", reply_markup=kb_ai_types())


async def show_cat(msg: Message, state: FSMContext):
    data = await state.get_data()
    await state.set_state(Flow.choose_cat)
    await msg.answer("Шаг 3/4 — выберите категорию:", reply_markup=kb_categories(data["ai"]))


async def show_prompt(msg: Message, state: FSMContext):
    data = await state.get_data()
    await state.set_state(Flow.choose_prompt)
    await msg.answer("Шаг 4/4 — выберите готовый промт:", reply_markup=kb_prompts(data["ai"], data["cat"]))
