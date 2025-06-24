import logging

from os import getenv
from aiogram import Bot, F, Router
from aiogram.types import Message
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from src.database import get_db
from src.models import User, Post
from src.keyboards.inline.inline_admin import post_approval

load_dotenv()
router = Router(name="user_commands_router")
logger = logging.getLogger("tg_handlers")
admin_chat = getenv("ADMIN_CHAT_ID")

@router.message(F.text == "/start")
async def start_command(message: Message) -> None:
    logger.info("Пользователь id=%s нажал /start", message.from_user.id)

    await message.answer(
        text="Здравствуй, житель нашего прекрасного королевства! Отправь мне картинку и я доставлю ее нашему барону."
    )

@router.message(F.photo)
async def post_suggest(message: Message, bot: Bot) -> None:
    user = message.from_user
    db: Session = next(get_db())
    
    try:
        db_user = db.execute(select(User).filter_by(telegram_id=user.id)).scalar_one_or_none()
        if not db_user:
            db_user = User(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
        
        new_post = Post(
            content_type="photo",
            file_id=message.photo[-1].file_id,
            caption=message.caption,
            user_id=db_user.id
        )
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        
        await bot.send_message(
            chat_id=admin_chat,
            text=f"Предложен пост от {user.first_name} {user.last_name} | {user.username}"
        )
        if message.content_type == "photo":
            await bot.send_photo(
                chat_id=admin_chat,
                photo=new_post.file_id,
                caption=new_post.caption,
                reply_markup=post_approval
            )
            await message.reply(text="Вы нас балуете, милорд! Пост отправлен нашему горячо любимому барону...")
        # elif message.content_type == "video":
        #     await bot.send_video(
        #         chat_id=admin_chat, video=message.video.file_id, caption=message.caption, reply_markup=post_approval
        #     )
    
    except SQLAlchemyError:
        db.rollback()
        await message.reply(text="Ошибка при обработке поста. Попробуйте позже.")

