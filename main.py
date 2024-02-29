import asyncio
import json
from datetime import datetime
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart

from db import DataBase
from config import settings

bot = Bot(token=settings.BOT_TOKEN)
dispatcher = Dispatcher()
db = DataBase(settings.DB_NAME, settings.COLLECTION_NAME)


@dispatcher.message(CommandStart())
async def process_start(message: Message) -> None:
    await message.answer(f"Hi {message.from_user.first_name}!")


@dispatcher.message()
async def process_get_statistic_data(message: Message) -> None:
    try:
        received_json = json.loads(message.text)
        dt_from = datetime.strptime(received_json["dt_from"], "%Y-%m-%dT%H:%M:%S")
        dt_upto = datetime.strptime(received_json["dt_upto"], "%Y-%m-%dT%H:%M:%S")
        group_type = received_json["group_type"]
        answer = db.get_statistic_data(dt_from, dt_upto, group_type)
        await message.answer(json.dumps(answer))

    except (ValueError, TypeError):
        await message.answer(
            "Невалидный запрос. Пример запроса:\n "
            '{"dt_from": "2022-09-01T00:00:00", '
            '"dt_upto": "2022-12-31T23:59:00", '
            '"group_type": "month"}'
        )

async def main() -> None:
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)
    dispatcher.run_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
