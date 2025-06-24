from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class DatabaseMiddleware(BaseMiddleware):
    """Миддлварь прокидывающий сессию соединения с базой в хендлеры."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> None:
        """Вызов основного функционала.

        Args:
            handler (Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]): Хендлер
            event (TelegramObject): Тип события
            data (dict[str, Any]): Доп. данные
        """
        async with data["session"]() as session:
            data["session"] = session
            await handler(event, data)
