from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)


def kb_start() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🧠 Выбрать Ассистента", callback_data="choose_ai")],
        ]
    )


def kb_global() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏠 Новая задача"),
             KeyboardButton(text="💾 История задач"),
             KeyboardButton(text="💳 Тарифы"),
             ]
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
    )


def kb_choice_task() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да", callback_data="new_task:yes")
            ],
            [
                InlineKeyboardButton(text="❌ Нет", callback_data="new_task:no")
            ],
        ]
    )


def kb_choice_history() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да", callback_data="history:yes")
            ],
            [
                InlineKeyboardButton(text="❌ Нет", callback_data="history:no")
            ],
        ]
    )
