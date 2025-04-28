from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from models.orm_models import Request
from utils.image_generation import replicate_anime


async def stylize_from_db(session: AsyncSession, request_id: int) -> Optional[bytes]:
    req: Request | None = await session.get(Request, request_id)
    if not req:
        print(f"Request {request_id} not found")
        return None
    return await replicate_anime(req.input_file)
