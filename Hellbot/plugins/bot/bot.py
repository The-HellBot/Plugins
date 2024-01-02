import heroku3
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, Message

from Hellbot import HEROKU_APP
from Hellbot.core import LOGS
from Hellbot.functions.tools import restart

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


@hellbot.bot.on_message(filters.command("restart") & Config.AUTH_USERS)
async def restart_clients(_, message: Message):
    await message.reply_text("Restarted Bot Successfully ✅")
    try:
        if HEROKU_APP:
            try:
                heroku = heroku3.from_key(Config.HEROKU_APIKEY)
                app = heroku.apps()[Config.HEROKU_APPNAME]
                app.restart()
            except:
                await restart()
        else:
            await restart()
    except Exception as e:
        LOGS.error(e)


BotHelp("Others").add(
    "start", "To start the bot and get the main menu."
).add(
    "help", "To get the help menu with all the command for this assistant bot."
).add(
    "restart", "To restart the bot."
).info(
    "Some basic commands of the bot."
).done()
