import logging

from os import getenv

from aiogram import Bot, F, Router
from aiogram.types import Message
from dotenv import load_dotenv

from src.keyboards.inline.inline_admin import post_approval


logger = logging.getLogger("tg_handlers")

router = Router(name="user_commands_router")

load_dotenv()
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
    logger.info("Пользователь id=%s загрузил пост", user.id)

    await bot.send_message(
        chat_id=admin_chat, text=f"Предложен пост от {user.first_name} {user.last_name} | {user.username}"
    )
    if message.content_type == "photo":
        await bot.send_photo(
            chat_id=admin_chat, photo=message.photo[-1].file_id, caption=message.caption, reply_markup=post_approval
        )
        await message.reply(text="Вы нас балуете, милорд! Пост отправлен нашему горячо любимому барону...")
        logger.info("Пост передан в канал админа id=%s, пользователь уведомлен", admin_chat)
    # elif message.content_type == "video":
    #     await bot.send_video(
    #         chat_id=admin_chat, video=message.video.file_id, caption=message.caption, reply_markup=post_approval
    #     )
