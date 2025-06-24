import logging
import time

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.database.engine import AsyncSessionLocal


logger = logging.getLogger("database")


class DatabaseMiddleware(BaseMiddleware):
    """Миддлварь прокидывающий сессию соединения с базой в хендлеры."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any | None:
        """Вызов основного функционала.

        Args:
            handler (Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]): Хендлер
            event (TelegramObject): Тип события
            data (dict[str, Any]): Доп. данные
        """
        async with AsyncSessionLocal() as session:
            data["session"] = session
            try:
                start = time.monotonic()
                result = await handler(event, data)

                await session.commit()
                duration = time.monotonic() - start

                logger.info(
                    "Транзакция успешно завершена",
                    extra={"handler": handler.__name__, "duration_sec": round(duration, 3)},
                )

                if duration > 3.0:
                    logger.warning(
                        "Медленная транзакция",
                        extra={"handler": handler.__name__, "duration_sec": round(duration, 3)},
                    )

                return result
            except Exception as e:
                await session.rollback()

                logger.error(
                    "Транзакция завершилась ошибкой",
                    extra={"handler": handler.__name__, "error": str(e), "error_type": e.__class__.__name__},
                    exc_info=True,
                )
