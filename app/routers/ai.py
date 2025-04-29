from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from states import Flow
from keyboards.ai_keyboards import (
    kb_ai_types,
    kb_categories,
    kb_prompts,
    kb_start_chat,
    kb_chat_back,
    kb_ai_types_with_history
)
from keyboards.main_keyboards import kb_start, kb_global
from promt.start_promt import WELCOME_TEXT

ai_picker_router = Router(name="ai_picker")


async def ai_entry(msg: Message, state: FSMContext) -> None:
    await state.set_state(Flow.choose_ai)
    await msg.answer("Шаг 1/3 — выберите тип ИИ:", reply_markup=kb_ai_types_with_history())


@ai_picker_router.callback_query(Flow.choose_ai, F.data.startswith("ai:"))
async def choose_ai(cb: CallbackQuery, state: FSMContext) -> None:
    _, code = cb.data.split(":", 1)

    if code == "back":
        await cb.answer()
        await cb.message.edit_reply_markup(reply_markup=None)
        await cb.message.answer(WELCOME_TEXT, reply_markup=kb_start())
        await cb.message.answer("\u2063", reply_markup=kb_global())
        return

    await state.update_data(ai_type=code)
    await state.set_state(Flow.choose_cat)
    await cb.answer()
    await cb.message.edit_text(
        "Шаг 2/3 — выберите категорию ассистента:",
        reply_markup=kb_categories(code),
    )


@ai_picker_router.callback_query(Flow.choose_cat, F.data.startswith("cat:"))
async def choose_cat(cb: CallbackQuery, state: FSMContext) -> None:
    _, code = cb.data.split(":", 1)

    if code == "back":
        await state.set_state(Flow.choose_ai)
        await cb.answer()
        await cb.message.edit_text(
            "Шаг 1/3 — выберите тип ИИ:", reply_markup=kb_ai_types()
        )
        return

    await state.update_data(cat=code)
    await state.set_state(Flow.choose_prompt)
    await cb.answer()
    await cb.message.edit_text(
        "Шаг 3/3 — выберите готовый промт:",
        reply_markup=kb_prompts(code),
    )


@ai_picker_router.callback_query(Flow.choose_prompt, F.data.startswith("pr:"))
async def choose_prompt(cb: CallbackQuery, state: FSMContext) -> None:
    _, code = cb.data.split(":", 1)

    if code == "back":
        data = await state.get_data()
        await state.set_state(Flow.choose_cat)
        await cb.answer()
        await cb.message.edit_text(
            "Шаг 2/3 — выберите категорию ассистента:",
            reply_markup=kb_categories(data["ai_type"]),
        )
        return

    await state.update_data(prompt=code)
    await cb.answer()
    await cb.message.edit_text(
        "Готово! Выбраны:\n"
        f"• ИИ: <b>{(await state.get_data())['ai_type']}</b>\n"
        f"• Категория: <b>{(await state.get_data())['cat']}</b>\n"
        f"• Промт: <b>{code}</b>\n\n"
        "Нажмите «Начать чат», отправьте текст запроса — получите заглушку-ответ.",
        reply_markup=kb_start_chat(),
    )


@ai_picker_router.callback_query(Flow.choose_prompt, F.data == "confirm:back")
async def confirm_back(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    await state.set_state(Flow.choose_prompt)
    await cb.answer()
    await cb.message.edit_text(
        "Шаг 3/3 — выберите готовый промт:",
        reply_markup=kb_prompts(data["cat"]),
    )


@ai_picker_router.callback_query(F.data == "chat:start")
async def chat_start(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.answer("Отправьте текст запроса")
    await cb.message.edit_reply_markup(reply_markup=None)
    await cb.message.answer(
        "Введите ваш запрос:",
        reply_markup=kb_chat_back(),
    )


@ai_picker_router.callback_query(F.data == "chat:back")
async def chat_back(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    await state.set_state(Flow.choose_prompt)
    await cb.answer()
    await cb.message.answer(
        "Готово! Выбраны:\n"
        f"• ИИ: <b>{data['ai_type']}</b>\n"
        f"• Категория: <b>{data['cat']}</b>\n"
        f"• Промт: <b>{data['prompt']}</b>\n\n"
        "Нажмите «Начать чат», чтобы снова отправить запрос.",
        reply_markup=kb_start_chat(),
    )


@ai_picker_router.message(Flow.choose_prompt)
async def dummy_answer(msg: Message, state: FSMContext) -> None:
    data = await state.get_data()
    reverse = msg.text.strip()[::-1] or "🤖 (пусто)"
    await msg.answer(
        f"Ответ <b>{data['ai_type']}-{data['prompt']}</b> → {reverse}",
        reply_markup=kb_chat_back()
    )


@ai_picker_router.callback_query(Flow.choose_ai, F.data.startswith("history:"))
async def history_view(cb: CallbackQuery, state: FSMContext) -> None:
    page = int(cb.data.split(":")[1])
    mock_tasks = [
        ("text", "ads", "📝 Рекламный текст"),
        ("image", "ghibli", "🎨 Стилизованное фото"),
        ("audio", "tts", "🗣️ Озвучка голосом"),
        ("video", "edit", "🎬 Монтаж ролика"),
        ("text", "summ", "📰 Краткое содержание"),
    ][(page-1)*3 : page*3]  # только 3 на страницу

    kb = [
        [InlineKeyboardButton(text=title, callback_data=f"restore:{ai}:{prompt}")]
        for ai, prompt, title in mock_tasks
    ]
    kb.append([
        InlineKeyboardButton(text="⬅️", callback_data=f"history:{max(1, page - 1)}"),
        InlineKeyboardButton(text="➡️", callback_data=f"history:{page + 1}"),
    ])
    kb.append([
        InlineKeyboardButton(text="🔙 Назад", callback_data="ai:back")
    ])

    await cb.answer()
    await cb.message.edit_text(
        f"🗂 История задач (страница {page})",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=kb)
    )


@ai_picker_router.callback_query(Flow.choose_ai, F.data.startswith("restore:"))
async def restore_prev(cb: CallbackQuery, state: FSMContext) -> None:
    _, ai_type, prompt = cb.data.split(":")
    await state.update_data(ai_type=ai_type, prompt=prompt)

    await cb.answer("Восстановлено из истории")
    await cb.message.edit_text(
        f"🔄 Восстановлено из истории:\n"
        f"• ИИ: <b>{ai_type}</b>\n"
        f"• Промт: <b>{prompt}</b>\n\n"
        "Введите новый текст — продолжим работу.",
        reply_markup=kb_chat_back()
    )
    await state.set_state(Flow.choose_prompt)
