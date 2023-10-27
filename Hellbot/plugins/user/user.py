from pyrogram.types import Message

from Hellbot.core import hellbot

from ..decorator import on_message


@on_message(["alive"], allow_sudo=True)
async def alive(_, message: Message):
    await hellbot.edit_or_reply(message, "Hellbot is alive!")
