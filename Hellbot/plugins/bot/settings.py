from pyrogram import filters
from pyrogram.types import Message

from Hellbot.core import Config, hellbot

from ..btnsK import SETTINGS_KB


@hellbot.bot.on_message(
    filters.command("settings") & Config.AUTH_USERS & filters.private
)
async def addclient(_, message: Message):
    await message.reply_text("**⚙️ Settings Menu:**", reply_markup=SETTINGS_KB)
