"""Роутеры команд администраторов."""

import logging

from os import getenv

from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update

from src.database.models import Post, PostStatus
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

    message = callback.message
    file_id = message.photo[-1].file_id
    await session.execute(update(Post).where(Post.file_id == file_id).values(status=PostStatus.PUBLISHED.value))
    result = await session.execute(select(Post.user_id).where(Post.file_id == file_id))
    user_id = result.scalar_one_or_none()
    if user_id:
        await bot.send_message(chat_id=int(user_id), text="Ваше предложение было одобрено.")

    await bot.send_photo(chat_id=channel_id, photo=message.photo[-1].file_id, caption=message.caption)
    
    await callback.answer("Пост опубликован")
    logger.info("Пост опубликован в канал id=%s", channel_id)


@router.callback_query(F.data == "post_declined")
async def decline_post(callback: CallbackQuery, bot: Bot, session: AsyncSession) -> None:
    logger.info("Админ id=%s отклонил публикацию", admin_id)
    await callback.message.edit_reply_markup(reply_markup=None)
    
    message = callback.message
    file_id = message.photo[-1].file_id
    await session.execute(update(Post).where(Post.file_id == file_id).values(status=PostStatus.DECLINED.value))
    result = await session.execute(select(Post.user_id).where(Post.file_id == file_id))
    user_id = result.scalar_one_or_none()
    if user_id:
        await bot.send_message(chat_id=int(user_id), text="Ваше предложение было отклонено.")

    await callback.answer("Пост отклонен")
