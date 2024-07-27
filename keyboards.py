from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

admin_statistic_btn_text = "📊 Statistic"


def format_kb(formats: list):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"🎞 {format_['format_note']}: {format_['filesize'] / 1024 / 1024:.2f} MB",
                    callback_data=f"format_{format_['format_id']}"
                )
            ]
            for format_ in formats
        ]
    )
    return kb


admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=admin_statistic_btn_text)
        ]
    ],
    resize_keyboard=True
)
