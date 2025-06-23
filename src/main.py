"""Стартовый модуль бота."""

import asyncio
import logging

from os import getenv

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from src.handlers.admin import router as admin_router
from src.handlers.user import router as user_router

from .logging_conf import configure_logger


dp = Dispatcher()


async def main() -> None:
    """Запуск телеграм бота."""
    dp.include_router(admin_router)
    dp.include_router(user_router)

    bot = Bot(token=getenv("BOT_TOKEN"))
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        load_dotenv()
        configure_logger()
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.error(msg=str(e), stack_info=True)
