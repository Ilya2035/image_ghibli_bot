from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "sqlite+aiosqlite:///bot_database.db"

engine = create_async_engine(DATABASE_URL, echo=True)
