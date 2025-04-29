from sqlalchemy import insert, select
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

    # Сразу создаем баланс с 100 токенами
    await session.execute(
        insert(UserBalance)
        .values(user_id=user.id, balance=100)
    )

    await session.commit()
    return user

