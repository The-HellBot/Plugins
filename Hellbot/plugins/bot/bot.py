from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, Message

from ..btnsG import gen_bot_help_buttons, start_button
from . import HELP_MSG, START_MSG, BotHelp, Config, hellbot


@hellbot.bot.on_message(filters.command("start") & Config.AUTH_USERS)
async def start_pm(_, message: Message):
    btns = start_button()

    await message.reply_text(
        START_MSG.format(message.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(btns),
    )


@hellbot.bot.on_message(filters.command("help") & Config.AUTH_USERS)
async def help_pm(_, message: Message):
    btns = gen_bot_help_buttons()

    await message.reply_text(
        HELP_MSG,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(btns),
    )


BotHelp("Others").add(
    "start", "To start the bot and get the main menu."
).add(
    "help", "To get the help menu with all the command for this assistant bot."
).info(
    "Some basic commands of the bot."
).done()
