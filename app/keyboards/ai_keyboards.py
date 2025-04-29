from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Шаг 1 — тип ИИ
AI_TYPES: list[tuple[str, str]] = [
    ("text",  "📝 Текст"),
    ("image", "🖼️ Изображения"),
    ("audio", "🎙️ Аудио"),
    ("video", "🎬 Видео"),
]

# Шаг 2 — категория ассистента (пример)
CATEGORIES: dict[str, list[tuple[str, str]]] = {
    "text":  [("copy",   "✍️ Копирайтинг"), ("summ", "📰 Суммаризация")],
    "image": [("style",  "🎨 Стилизация"),  ("gen",  "🌄 Генерация")],
    "audio": [("stt",    "🔤 Расшифровка"), ("tts",  "🗣️ Озвучка")],
    "video": [("edit",   "✂️ Монтаж"),      ("gen",  "🎞️ Генерация")],
}

# Шаг 3 — промты-заглушки
PROMPTS: dict[str, list[tuple[str, str]]] = {
    "copy": [("ads", "Рекламный текст"), ("blog", "Статья-1000 с")],
    "summ": [("short", "Сжать до 1 абзаца"), ("key", "Ключевые тезисы")],
    "style": [("ghibli", "Стиль Ghibli"), ("oil", "Масляная живопись")],
    # … остальные по аналогии …
}


def kb_ai_types() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=label, callback_data=f"ai:{code}")]
            for code, label in AI_TYPES
        ] + [[InlineKeyboardButton(text="🔙 Назад", callback_data="ai:back")]],
    )


def kb_categories(ai_code: str) -> InlineKeyboardMarkup:
    from .ai_keyboards import CATEGORIES
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=label, callback_data=f"cat:{code}")]
            for code, label in CATEGORIES.get(ai_code, [])
        ] + [[InlineKeyboardButton(text="🔙 Назад", callback_data="cat:back")]],
    )


def kb_prompts(cat_code: str) -> InlineKeyboardMarkup:
    from .ai_keyboards import PROMPTS
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=label, callback_data=f"pr:{code}")]
            for code, label in PROMPTS.get(cat_code, [])
        ] + [[InlineKeyboardButton(text="🔙 Назад", callback_data="pr:back")]],
    )


def kb_start_chat() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🏁 Начать чат", callback_data="chat:start"),
                InlineKeyboardButton(text="🔙 Назад",     callback_data="confirm:back"),
            ]
        ]
    )


def kb_chat_back() -> InlineKeyboardMarkup:
    """Inline-кнопка «🔙 Назад» на этапе ввода текста."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="chat:back")]
        ]
    )


def kb_ai_types_with_history(page: int = 1) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=label, callback_data=f"ai:{code}")]
            for code, label in AI_TYPES
        ] + [
            [InlineKeyboardButton(text="🗂 История задач", callback_data=f"history:{page}")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="ai:back")]
        ]
    )
