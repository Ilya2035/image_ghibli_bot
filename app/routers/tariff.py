from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards.tariff_keyboards import kb_balance
from crud.get_balance_transactions import get_balance
from crud.user_transactions import add_tokens
from db.session import async_session

tariff_router = Router(name="tariff")


@tariff_router.message((F.text == "💳 Тарифы") | (F.text == "/tariff"))
async def tariff_entry(msg: Message) -> None:
    tokens = await get_balance(msg.from_user.id)
    await msg.answer(
        f"На вашем счёте <b>{tokens}</b> токенов.\n"
        "Нажмите «Пополнить», чтобы купить ещё.",
        reply_markup=kb_balance(),
    )


@tariff_router.callback_query(F.data == "topup")
async def topup(cb: CallbackQuery) -> None:
    async with async_session() as session:
        new_balance = await add_tokens(session, str(cb.from_user.id), amount=100)
        await session.commit()

    await cb.answer("Баланс пополнен на 100 токенов! 🎉")
    await cb.message.answer(
        f"Теперь у вас <b>{new_balance}</b> токенов.\n"
        "Можете продолжить создавать запросы",
    )
