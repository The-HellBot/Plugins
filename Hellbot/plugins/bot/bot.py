from pyrogram import filters
from pyrogram.types import Message

from Hellbot.core import Config, hellbot


@hellbot.bot.on_message(filters.command("start") & Config.AUTH_USERS & filters.private)
async def start_pm(_, message: Message):
    await message.reply_text("Hii")
