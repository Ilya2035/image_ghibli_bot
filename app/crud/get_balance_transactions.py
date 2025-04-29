from db.session import async_session
from sqlalchemy import select
from models.orm_models import User, UserBalance


async def get_balance(tg_id: int) -> int:
    async with async_session() as session:
        result = await session.execute(
            select(UserBalance.balance)
            .join(User)
            .where(User.user_id == str(tg_id))
        )
        balance = result.scalar_one_or_none()
        return balance if balance is not None else 0
