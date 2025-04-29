from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards.tariff_keyboards import kb_balance
from crud.get_balance_transactions import get_balance

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
    await cb.answer("Функция пополнения пока в разработке! 🚧", show_alert=True)
