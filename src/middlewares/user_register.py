import logging

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User as TgUser
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User


logger = logging.getLogger("database")


class UserRegisterMiddleware(BaseMiddleware):
    """Миддлварь регистрирующий пользователей использующих бота."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        """Вызов основного функционала.

        Args:
            handler (Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]): Хендлер
            event (TelegramObject): Тип события
            data (dict[str, Any]): Доп. данные
        """
        user: TgUser | None = data.get("event_from_user")
        session: AsyncSession = data["session"]

        if not user:
            return await handler(event, data)

        db_user = await session.execute(select(User).where(User.telegram_id == user.id))
        db_user: User | None = db_user.scalar_one_or_none()

        if not db_user:
            db_user = User(
                telegram_id=user.id, username=user.username, first_name=user.first_name, last_name=user.last_name
            )
            session.add(db_user)
        else:
            upd_fields = {}
            if db_user.username != user.username:
                upd_fields["username"] = user.username
            if db_user.first_name != user.first_name:
                upd_fields["first_name"] = user.first_name
            if db_user.last_name != user.last_name:
                upd_fields["last_name"] = user.last_name

            if upd_fields:
                await session.execute(update(User).where(User.telegram_id == user.id).values(**upd_fields))

        return await handler(event, data)
