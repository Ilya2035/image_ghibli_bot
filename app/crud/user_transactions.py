from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.orm_models import User


async def add_user(session: AsyncSession, tg_id: str) -> User:
    user = await session.scalar(
        select(User).where(User.user_id == tg_id)
    )
    if user:
        return user

    result = await session.execute(
        insert(User).values(user_id=tg_id).returning(User)
    )
    await session.commit()
    return result.scalar_one()
