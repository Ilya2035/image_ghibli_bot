from db.engine import engine
from models.orm_models import Base


async def init_db() -> None:
    """Создаёт все таблицы, если их ещё нет."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
