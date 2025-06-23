from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


post_approval = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Запостить ✅", callback_data="post_approve"),
            InlineKeyboardButton(text="Оклонить ❌", callback_data="post_declined"),
        ]
    ]
)
