import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import settings
from router import router

bot = Bot(token=settings.BOT_TOKEN)
dispatcher = Dispatcher()
dispatcher.include_router(router)


async def main() -> None:
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)
    dispatcher.run_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
