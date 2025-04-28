from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def main_menu_kb():
    kb = [
        [InlineKeyboardButton(text="О Латокен", callback_data="latoken")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=kb)
