import uuid
import io

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart
import asyncio

from aiogram.enums.parse_mode import ParseMode


from src.app.video.analyzer import start_video_analyzer
from src.shared.configs import PROJECT_SETTINGS

from .handlers._detection_drone import detection_drone_handler


USER_TOKEN = PROJECT_SETTINGS.telegram_bot.user_token
SERVICE_TOKEN = PROJECT_SETTINGS.telegram_bot.service_token
TARGET_CHAT_ID = -4764676516

user_bot = Bot(token=USER_TOKEN)
dp = Dispatcher()

service_bot = Bot(token=SERVICE_TOKEN)


from aiogram.filters import Command
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import F

from src.shared.libs.utils import generate_task_id


from src.shared.api.logger import Logger

from src.shared.api.save_video_info import save_video_info_api


logger = Logger


@dp.message(lambda msg: msg.video is not None or msg.animation is not None)
async def detection_drone(message: Message):

    if message.video:
        file_id = message.video.file_id
    elif message.animation:
        file_id = message.animation.file_id
    else:
        return await message.answer("Неккоректный формат сообщения!")

    await detection_drone_handler(user_bot, service_bot, TARGET_CHAT_ID, file_id)


async def main():
    logger.info("Telegram Bot Started")
    await dp.start_polling(user_bot)


if __name__ == "__main__":
    asyncio.run(main())
