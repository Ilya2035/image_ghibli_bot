from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def kb_balance() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Пополнить", callback_data="topup")],
        ]
    )
