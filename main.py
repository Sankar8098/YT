import asyncio
import logging
import sys
import yt_dlp
import os

from environs import Env

from aiogram import Bot, Dispatcher, html, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.utils.chat_action import ChatActionSender

from download import get_video_info
from keyboards import format_kb, admin_kb, admin_statistic_btn_text
from db import User, db

env = Env()
env.read_env()

TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!\n\nSend me a link to the YouTube video.")
    user, created = User.get_or_create(chat_id=message.chat.id, defaults={'lang': 'en', 'is_active': True})

    if str(message.chat.id) in ADMINS:
        await message.answer("You are an admin.", reply_markup=admin_kb)

    if created:
        for admin in ADMINS:
            await bot.send_message(admin, f"New user: {message.from_user.full_name} ({message.chat.id})")


@dp.message(F.text == admin_statistic_btn_text)
async def admin_statistic_handler(message: Message) -> None:
    if str(message.chat.id) not in ADMINS:
        return

    users = User.select().count()
    await message.answer(f"📊 Statistic\n\n Users: {users}", reply_markup=admin_kb)


@dp.message()
async def getlink_handler(message: Message) -> None:
    global link
    global video_info
    link = message.text
    video_info = get_video_info(link)
    await message.delete()

    if video_info is None:
        await message.answer("Error: Unable to get video information.")
        return

    formats = video_info['formats']
    formats = [format_ for format_ in formats if
               'filesize' in format_ and format_['filesize'] is not None and format_['ext'] == 'mp4' and format_[
                   'height'] >= 480]
    video_formats_text = ''
    for format_ in formats:
        video_formats_text += f"⚡️<code>{format_['format_note']}: {format_['filesize'] / 1024 / 1024:.2f} MB</code>\n"

    caption_text = (f"📹 {video_info['title']}\n"
                    f"👤 <a href='{video_info['channel_url']}'>@{video_info['uploader']}</a>\n\n"
                    f"{video_formats_text}\n\n"
                    f"Download formats ↓")

    await message.answer_photo(video_info['thumbnail'], caption=caption_text, reply_markup=format_kb(formats))


@dp.callback_query(F.data.startswith("format_"))
async def format_callback_handler(query: types.CallbackQuery) -> None:
    format_id = query.data.split("_")[1]
    await query.message.delete()
    loading = await query.message.answer("⚠️ Video size is large. Please wait for a while. \n\nDownloading...")

    ydl_opts = {
        'format': format_id,
        'outtmpl': 'output/video/%(title)s.%(ext)s',
        'quiet': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
            info_dict = ydl.extract_info(link)
            title = ydl.prepare_filename(info_dict).split('/')[-1]  # Get only the filename
            file_path = f'output/video/{title}'

            if os.path.exists(file_path):
                await loading.delete()
                try:
                    video = FSInputFile(file_path)
                    async with ChatActionSender(bot=bot, chat_id=query.from_user.id, action="upload_video"):
                        await query.message.answer_video(video=video,
                                                         caption=f"📹 {video_info['title']}\n👤 <a href='{video_info['channel_url']}'>@{video_info['uploader']}</a> \n\n"
                                                                 f"📥 video downloaded by @mega_youtube_downloader_bot")
                except Exception as e:
                    logging.error(f"Error: {e}")
                    await query.message.answer("Error: Failed to send the video.")
                os.remove(file_path)
            else:
                await loading.delete()
                await query.message.answer("Error: Video file not found.")
    except Exception as e:
        logging.error(f"Error: {e}")
        await loading.delete()
        await query.message.answer("Error: Failed to download or send the video.")


async def main() -> None:
    db.connect()
    db.create_tables([User])
    db.close()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
