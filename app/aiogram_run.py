import asyncio

from create_bot import bot, dp
from routers.start import start_router
from routers.ghibli import photo_router
from routers.tariff import tariff_router
from routers.ai import ai_router
from routers.history import history_router
from db.init_db import init_db


async def main() -> None:
    await init_db()
    dp.include_router(start_router)
    # dp.include_router(photo_router)
    dp.include_router(tariff_router)
    dp.include_router(history_router)
    dp.include_router(ai_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
