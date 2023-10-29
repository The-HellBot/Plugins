from pyrogram.types import Message

from Hellbot.core import hellbot

from . import HelpMenu, on_message


@on_message("alive", allow_sudo=True)
async def alive(_, message: Message):
    await hellbot.edit(message, "Hellbot is alive!")


HelpMenu("alive").add(
    "alive", None, "Get the alive message of the bot.", "alive"
).info(
    "Alive Menu"
).done()
