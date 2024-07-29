from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

admin_statistic_btn_text = "📊 Statistic"


def format_kb(formats: list):
    builder = InlineKeyboardBuilder()
    for format_ in formats:
        builder.button(text=f"🎞 {format_.resolution}", callback_data=f"format_{format_.itag}")

    builder.button(text="🔊 Audio", callback_data="format_audio")
    builder.button(text="🖼 Thumbnail", callback_data="format_thumbnail")
    builder.adjust(2)
    return builder.as_markup()


admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=admin_statistic_btn_text)
        ]
    ],
    resize_keyboard=True
)
