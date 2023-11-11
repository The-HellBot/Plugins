import time

from pyrogram.types import Message

from Hellbot import START_TIME
from Hellbot.core import ENV, db, hellbot
from Hellbot.functions.formatter import readable_time

from .. import PING_TEXT
from . import HelpMenu, on_message


@on_message("alive", allow_sudo=True)
async def alive(_, message: Message):
    await hellbot.edit(message, "Hellbot is alive!")


@on_message("ping", allow_sudo=True)
async def ping(_, message: Message):
    start_time = time.time()
    hell = await hellbot.edit(message, "**Pong ~**")
    uptime = readable_time(time.time() - START_TIME)
    img = await db.get_env(ENV.ping_pic)
    end_time = time.time()
    speed = end_time - start_time
    if img:
        await message.reply_document(
            img,
            caption=PING_TEXT.format(
                round(speed, 3), uptime, message.from_user.mention
            ),
            force_document=False,
        )
        return
    await hellbot.edit(hell, PING_TEXT.format(round(speed, 3), uptime, message.from_user.mention))


HelpMenu("bot").add("alive", None, "Get the alive message of the bot.", "alive").add(
    "ping",
    None,
    "Check the ping speed and uptime of bot.",
    "ping",
    "You can also customize ping message by adding a media to it.",
).info("Alive Menu").done()
