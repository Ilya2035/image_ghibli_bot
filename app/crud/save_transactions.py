from typing import Optional
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from models.orm_models import Request


async def save_output_to_db(
    session: AsyncSession,
    request_id: int,
    output_bytes: Optional[bytes],
) -> None:
    status = "done" if output_bytes else "error"
    await session.execute(
        update(Request)
        .where(Request.id == request_id)
        .values(output_file=output_bytes, status=status)
    )
    await session.commit()
