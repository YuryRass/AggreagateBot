import json
from datetime import datetime

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import settings
from db import DataBase

router = Router()

db = DataBase(settings.DB_NAME, settings.COLLECTION_NAME)


@router.message(CommandStart())
async def process_start(message: Message) -> None:
    await message.answer(f'Hi {message.from_user.first_name}!')


@router.message()
async def process_get_statistic_data(message: Message) -> None:
    try:
        received_json = json.loads(message.text)
        dt_from = datetime.strptime(received_json['dt_from'], '%Y-%m-%dT%H:%M:%S')
        dt_upto = datetime.strptime(received_json['dt_upto'], '%Y-%m-%dT%H:%M:%S')
        group_type = received_json['group_type']
        answer = db.get_statistic_data(dt_from, dt_upto, group_type)
        await message.answer(json.dumps(answer))

    except (ValueError, TypeError):
        await message.answer(
            'Невалидный запрос. Пример запроса:\n '
            '{"dt_from": "2022-09-01T00:00:00", '
            '"dt_upto": "2022-12-31T23:59:00", '
            '"group_type": "month"}'
        )
