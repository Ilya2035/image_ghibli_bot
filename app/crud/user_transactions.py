from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.orm_models import User


async def add_user(session: AsyncSession, tg_id: str) -> User:
    result = await session.execute(
        insert(User)
        .values(user_id=tg_id)
        .on_conflict_do_nothing()
        .returning(User)
    )
    user = result.scalar_one_or_none()

    if user is None:
        user = await session.scalar(select(User).where(User.user_id == tg_id))

    await session.commit()
    return user
