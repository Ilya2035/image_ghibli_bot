from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from prompt.types_of_ai import text, image, audio, video

AI_TYPES = [
    ("text", "📝 Текст"),
    ("image", "🖼️ Изображения"),
    ("audio", "🎙️ Аудио"),
    ("video", "🎬 Видео"),
]

TYPES = {
    "text": text.CATEGORIES,
    "image": image.CATEGORIES,
    "audio": audio.CATEGORIES,
    "video": video.CATEGORIES,
}

PROMPTS_MAP = {
    "text": text.PROMPTS,
    "image": image.PROMPTS,
    "audio": audio.PROMPTS,
    "video": video.PROMPTS,
}


def kb_mode() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💬 Диалог", callback_data="mode:dialog")],
            [InlineKeyboardButton(text="🔎 Запрос", callback_data="mode:single")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="mode:back")],
        ]
    )


def kb_ai_types() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text=label, callback_data=f"ai:{code}")]
        for code, label in AI_TYPES
    ]
    keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data="mode:back")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def kb_categories(ai_code: str) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text=label, callback_data=f"cat:{code}")]
        for code, label in TYPES.get(ai_code, [])
    ]
    keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data="ai:back")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def kb_prompts(ai_code: str, cat_code: str) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text=label, callback_data=f"pr:{code}")]
        for code, label in PROMPTS_MAP.get(ai_code, {}).get(cat_code, [])
    ]
    keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data="cat:back")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
