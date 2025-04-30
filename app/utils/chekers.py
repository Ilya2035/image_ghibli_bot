from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import Flow


async def delete_menu_if_not_in_prompt(msg: Message, state: FSMContext) -> None:
    """
    Если текущее состояние не Flow.choose_prompt, удаляет:
      1) Сообщение пользователя msg
      2) Предыдущее бот-сообщение (msg.message_id - 1)
    """
    current_state = await state.get_state()
    if current_state != Flow.choose_prompt.state:
        await msg.delete()
        await msg.bot.delete_message(msg.chat.id, msg.message_id - 1)


async def delete_menu_if_not_in_prompt(msg: Message, state: FSMContext) -> None:
    """
    Если текущее состояние не Flow.choose_prompt, удаляет:
      1) Сообщение пользователя (msg)
      2) Предыдущее бот-сообщение (msg.message_id - 1)
    """
    current_state = await state.get_state()
    if current_state != Flow.choose_prompt.state:
        try:
            await msg.delete()
        except Exception:
            pass
        try:
            await msg.bot.delete_message(msg.chat.id, msg.message_id - 1)
        except Exception:
            pass
