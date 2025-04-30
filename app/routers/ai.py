from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from states import Flow
from keyboards.ai_keyboards import kb_mode, kb_ai_types, kb_categories, kb_prompts
from utils.menu import show_welcome_menu
from utils.show_answers import show_mode, show_ai, show_cat, show_prompt
from utils.chekers import delete_menu_if_not_in_prompt
from prompt.choose_prompt import STEP_1, STEP_2, STEP_3, STEP_4
from crud.get_balance_transactions import get_balance
from crud.user_transactions import add_tokens
from db.session import async_session


ai_router = Router(name="ai_router")


@ai_router.message(F.text == "…кнопка запуска AI…")
async def ai_entry(msg: Message, state: FSMContext):
    await state.set_state(Flow.choose_mode)
    await msg.answer(STEP_1, reply_markup=kb_mode())


@ai_router.callback_query(Flow.choose_mode, F.data == "mode:back")
async def back_to_menu(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await cb.message.delete()
    await show_welcome_menu(cb.message, state)


@ai_router.callback_query(Flow.choose_ai, F.data == "mode:back")
async def back_to_mode(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await cb.message.delete()
    await show_mode(cb.message, state)


@ai_router.callback_query(Flow.choose_cat, F.data == "ai:back")
async def back_to_ai(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await cb.message.delete()
    await show_ai(cb.message, state)


@ai_router.callback_query(Flow.choose_prompt, F.data == "cat:back")
async def back_to_cat(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await cb.message.delete()
    await show_cat(cb.message, state)


# ——— Основная цепочка вперёд ———

@ai_router.callback_query(Flow.choose_mode, F.data.startswith("mode:"))
async def choose_mode(cb: CallbackQuery, state: FSMContext):
    _, mode = cb.data.split(":", 1)
    await state.update_data(mode=mode)
    await state.set_state(Flow.choose_ai)

    await cb.answer()
    await cb.message.edit_text(STEP_2, reply_markup=kb_ai_types())


@ai_router.callback_query(Flow.choose_ai, F.data.startswith("ai:"))
async def choose_ai(cb: CallbackQuery, state: FSMContext):
    _, ai_type = cb.data.split(":", 1)
    await state.update_data(ai=ai_type)
    await state.set_state(Flow.choose_cat)

    await cb.answer()
    await cb.message.edit_text(STEP_3, reply_markup=kb_categories(ai_type))


@ai_router.callback_query(Flow.choose_cat, F.data.startswith("cat:"))
async def choose_cat(cb: CallbackQuery, state: FSMContext):
    _, cat = cb.data.split(":", 1)
    await state.update_data(cat=cat)
    await state.set_state(Flow.choose_prompt)

    await cb.answer()
    data = await state.get_data()
    await cb.message.edit_text(STEP_4, reply_markup=kb_prompts(data["ai"], cat))


@ai_router.callback_query(Flow.choose_prompt, F.data.startswith("pr:"))
async def choose_prompt(cb: CallbackQuery, state: FSMContext):
    _, prompt = cb.data.split(":", 1)
    await state.update_data(prompt=prompt)
    await state.set_state(Flow.choose_prompt)

    data = await state.get_data()
    await cb.answer()
    await cb.message.edit_text(
        f"Вы выбрали:\n"
        f"• Режим: <b>{data['mode']}</b>\n"
        f"• ИИ: <b>{data['ai']}</b>\n"
        f"• Категория: <b>{data['cat']}</b>\n"
        f"• Промт: <b>{data['prompt']}</b>\n\n"
        "Теперь введите ваш текстовый запрос:"
    )


@ai_router.message(Flow.choose_prompt)
async def dummy_answer(msg: Message, state: FSMContext):
    await delete_menu_if_not_in_prompt(msg, state)

    tg_id = msg.from_user.id
    balance = await get_balance(tg_id)
    if balance < 10:
        return await msg.answer(f"❗ Недостаточно токенов (есть {balance}, нужно 10).")

    async with async_session() as session:
        new_balance = await add_tokens(session, str(tg_id), amount=-10)
        await session.commit()

    data = await state.get_data()
    text = msg.text or ""
    result = text[::-1]

    await msg.answer(
        f"ИИ: <b>{data['ai']}</b>\n"
        f"Категория: <b>{data['cat']}</b>\n"
        f"Промт: <b>{data['prompt']}</b>\n\n"
        f"Ответ: <code>{result}</code>\n\n"
        f"✅ Списано 10 токенов. Баланс: <b>{new_balance}</b>"
    )
