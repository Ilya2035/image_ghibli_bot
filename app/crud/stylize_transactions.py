from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from models.orm_models import Session
from utils.image_generation import replicate_image


async def stylize_from_db(session: AsyncSession, request_id: int) -> Optional[bytes]:

    req: Session | None = await session.get(Session, request_id)
    if req is None:
        return None

    if req.output_file:
        return req.output_file

    return await replicate_image(req.input_file)
