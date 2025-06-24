"""Роутеры команд администраторов."""

import logging

from os import getenv

from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database.models import Post
from src.filters import IsAdmin
from src.middlewares import DatabaseMiddleware


logger = logging.getLogger("tg_handlers")
load_dotenv()

channel_id = int(getenv("CHANNEL_ID"))
admin_id = int(getenv("ADMIN_ID"))

router = Router(name="admin_commands_router")
router.callback_query.filter(IsAdmin(admin_id))
router.callback_query.middleware(DatabaseMiddleware())


@router.callback_query(F.data == "post_approve")
async def approve_post(callback: CallbackQuery, bot: Bot, session: AsyncSession) -> None:
    logger.info("Админ id=%s одобрил публикацию", admin_id)
    await callback.message.edit_reply_markup(reply_markup=None)

    # FIXME: Зач это здесь? чето не увидел продолжения логики
    # post_id = hash(callback.data)
    # await session.execute(select(Post).filter_by(id=post_id))

    message = callback.message
    await bot.send_photo(chat_id=channel_id, photo=message.photo[-1].file_id, caption=message.caption)
    await callback.answer("Пост опубликован")
    logger.info("Пост опубликован в канал id=%s", channel_id)


@router.callback_query(F.data == "post_declined")
async def decline_post(callback: CallbackQuery, session: AsyncSession) -> None:
    logger.info("Админ id=%s отклонил публикацию", admin_id)
    await callback.message.edit_reply_markup(reply_markup=None)

    post_id = hash(callback.data)
    await session.delete(select(Post).filter_by(id=post_id))

    await callback.answer("Пост отклонен")
