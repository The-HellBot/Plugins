from pyrogram import filters
from pyrogram.types import Message

from Hellbot.core import Config, hellbot

from . import START_MSG


@hellbot.bot.on_message(filters.command("start") & Config.AUTH_USERS & filters.private)
async def start_pm(_, message: Message):
    await message.reply_text(START_MSG)
