from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from models.orm_models import Request


async def add_photo_request(
    session: AsyncSession,
    *,
    user_id: int,
    photo_bytes: bytes,
) -> Request:
    result = await session.execute(
        insert(Request)
        .values(
            user_id=user_id,
            input_file=photo_bytes,
            status="processing",
        )
        .returning(Request)
    )
    request = result.scalar_one()
    await session.flush()
    return request
