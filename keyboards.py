from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

admin_statistic_btn_text = "📊 Statistic"
admin_send_btn_text = "📤 Send Message"


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
        ],
        [
            KeyboardButton(text=admin_send_btn_text)
        ]
    ],
    resize_keyboard=True
)


admin_confirm_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Confirm", callback_data="send_confirm"),
            InlineKeyboardButton(text="❌ Cancel", callback_data="send_cancel")
        ]
    ]
)