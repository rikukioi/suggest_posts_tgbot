from os import getenv
from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from src.database import get_db
from src.models import Post
from src.filters import IsAdmin

load_dotenv()

channel_chat = int(getenv("CHANNEL_ID"))
admin_id = int(getenv("ADMIN_ID"))

router = Router(name="admin_commands_router")
router.message.filter(IsAdmin(admin_id))
router.callback_query.filter(IsAdmin(admin_id))

@router.callback_query(F.data.startswith("post_approve:"))
async def approve_post(callback: CallbackQuery, bot: Bot) -> None:
    await callback.message.edit_reply_markup(reply_markup=None)
    db: Session = next(get_db())
    
    post_id = int(callback.data.split(":")[1])
    post = db.execute(select(Post).filter_by(id=post_id)).scalar_one_or_none()
    
    if post:
        post.approved = True
        db.commit()
        await bot.send_photo(chat_id=channel_chat, photo=post.file_id, caption=post.caption)
        await callback.answer("Пост опубликован")
    else:
        await callback.answer("Пост не найден")

@router.callback_query(F.data.startswith("post_decline:"))
async def decline_post(callback: CallbackQuery) -> None:
    await callback.message.edit_reply_markup(reply_markup=None)
    post_id = int(callback.data.split(":")[1])
    db: Session = next(get_db())
    post = db.execute(select(Post).filter_by(id=post_id)).scalar_one_or_none()
    if post:
        db.delete(post)
        db.commit()
    await callback.answer("Пост отклонен")
    