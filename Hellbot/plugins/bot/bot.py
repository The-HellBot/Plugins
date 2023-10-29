from pyrogram import filters
from pyrogram.types import Message

from Hellbot.core import Config, hellbot

from ..btnsK import SETTINGS_KB
from . import START_MSG, BotHelp


@hellbot.bot.on_message(filters.command("start") & Config.AUTH_USERS & filters.private)
async def start_pm(_, message: Message):
    await message.reply_text(START_MSG)


@hellbot.bot.on_message(
    filters.command("settings") & Config.AUTH_USERS & filters.private
)
async def addclient(_, message: Message):
    await message.reply_text("**⚙️ 𝖲𝖾𝗍𝗍𝗂𝗇𝗀𝗌 𝖬𝖾𝗇𝗎:**", reply_markup=SETTINGS_KB)



BotHelp("Others").add(
    "start", "To check if bot alive or not."
).add(
    "settings", "To change settings of bot."
).info(
    "Some basic commands of the bot."
).done()
