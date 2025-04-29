from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)


def kb_start() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🧠 Выбрать ИИ", callback_data="choose_ai")],
        ]
    )


def kb_global() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏠 Меню"), KeyboardButton(text="💳 Тарифы")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
    )
