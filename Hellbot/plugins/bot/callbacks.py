from pyrogram import filters
from pyrogram.types import CallbackQuery

from Hellbot.core import Config, hellbot


@hellbot.bot.on_callback_query(filters.regex(r"auth_close") & Config.AUTH_USERS)
async def close(_, cb: CallbackQuery):
    await cb.message.delete()


@hellbot.bot.on_callback_query(filters.regex(r"close"))
async def close(_, cb: CallbackQuery):
    await cb.message.delete()
