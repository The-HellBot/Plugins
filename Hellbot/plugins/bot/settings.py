from pyrogram.types import Message
from Hellbot.core import hellbot
from pyrogram import filters
from ..btnsK import SETTINNGS_KB
from Hellbot.core import Config

@hellbot.bot.on_message(filters.command("settings") & Config.AUTH_USERS & filters.private)
async def addclient(_, message: Message):
    await message.reply_text("**⚙️ Settings Menu:**", reply_markup=SETTINNGS_KB)
