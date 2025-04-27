import asyncio
from create_bot import bot, dp
from handlers.start import start_router
from handlers.about_lotaken import about_lotaken
from handlers.hackathon import about_hackathon
from handlers.message_handler import message_router
from handlers.culture_deck import culture_router
from handlers.test_handler import test_router


async def main():
    dp.include_router(start_router)
    dp.include_router(about_lotaken)
    dp.include_router(about_hackathon)
    dp.include_router(culture_router)
    dp.include_router(message_router)
    dp.include_router(test_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
