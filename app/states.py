from aiogram.fsm.state import State, StatesGroup


class Flow(StatesGroup):
    choose_ai      = State()   # Шаг 1: текст / картинка / аудио / видео
    choose_cat     = State()   # Шаг 2: категория ассистента
    choose_prompt  = State()   # Шаг 3: конкретный промт
