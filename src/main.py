"""Стартовый модуль бота."""

import asyncio
import logging
import sys

from os import getenv

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from src.handlers.admin import router as admin_router
from src.handlers.user import router as user_router


dp = Dispatcher()


async def main() -> None:
    """Запуск телеграм бота."""
    dp.include_router(admin_router)
    dp.include_router(user_router)

    bot = Bot(token=getenv("BOT_TOKEN"))
    await dp.start_polling(bot)


if __name__ == "__main__":
    load_dotenv()
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.log(level=20, msg=str(e))
