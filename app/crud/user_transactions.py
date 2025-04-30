from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.orm_models import User, UserBalance


async def add_user(session: AsyncSession, tg_id: str) -> User:
    user = await session.scalar(select(User).where(User.user_id == tg_id))
    if user:
        return user

    result = await session.execute(
        insert(User)
        .values(user_id=tg_id)
        .returning(User)
    )
    user = result.scalar_one()

    await session.execute(
        insert(UserBalance)
        .values(id=user.id, balance=100)
    )

    await session.flush()
    return user


async def add_tokens(session: AsyncSession, tg_id: str, amount: int = 100) -> int:
    user = await session.scalar(select(User).where(User.user_id == tg_id))
    if not user:
        return 0  # или можно raise

    await session.execute(
        update(UserBalance)
        .where(UserBalance.id == user.id)
        .values(balance=UserBalance.balance + amount)
    )
    await session.flush()

    # Вернём новый баланс
    result = await session.execute(
        select(UserBalance.balance).where(UserBalance.id == user.id)
    )
    return result.scalar_one()
