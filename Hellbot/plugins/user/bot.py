import os
import time

from pyrogram import Client
from pyrogram.types import Message

from Hellbot import START_TIME
from Hellbot.core import ENV, db, hellbot
from Hellbot.functions.formatter import readable_time
from Hellbot.functions.images import generate_alive_image

from .. import PING_TEXT
from . import HelpMenu, on_message


@on_message("alive", allow_sudo=True)
async def alive(client: Client, message: Message):
    hell = await hellbot.edit(message, "Processing ...")
    if message.from_user.photo:
        user_pfp = await client.download_media(message.from_user.photo.big_file_id)
        del_path = True
    else:
        user_pfp = "./Hellbot/resources/images/hellbot_logo.png"
        del_path = False

    img = generate_alive_image(message.from_user.first_name, user_pfp, del_path)
    await message.reply_photo(img, caption="**Hellbot is alive ~**")
    await hell.delete()
    os.remove(img)


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
