import os
import random
import time

from pyrogram import Client
from pyrogram.types import Message

from Hellbot import START_TIME
from Hellbot.core import ENV, db, hellbot
from Hellbot.functions.formatter import readable_time
from Hellbot.functions.images import generate_alive_image
from Hellbot.functions.templates import alive_template, ping_template

from . import HelpMenu, on_message


@on_message("alive", allow_stan=True)
async def alive(client: Client, message: Message):
    hell = await hellbot.edit(message, "Processing ...")

    img = await db.get_env(ENV.alive_pic)
    if not img:
        if message.from_user.photo:
            user_pfp = await client.download_media(message.from_user.photo.big_file_id)
            del_path = True
        else:
            user_pfp = "./Hellbot/resources/images/hellbot_logo.png"
            del_path = False
        img = [generate_alive_image(message.from_user.first_name, user_pfp, del_path)]
    else:
        img = img.split(" ")

    img = random.choice(img)
    uptime = readable_time(time.time() - START_TIME)
    caption = await alive_template(client.me.first_name, uptime)

    await message.reply_photo(img, caption=caption)
    await hell.delete()

    try:
        os.remove(img)
    except:
        pass


@on_message("ping", allow_stan=True)
async def ping(client: Client, message: Message):
    start_time = time.time()
    hell = await hellbot.edit(message, "**Pong ~**")
    uptime = readable_time(time.time() - START_TIME)
    img = await db.get_env(ENV.ping_pic)
    end_time = time.time()
    speed = end_time - start_time
    caption = await ping_template(round(speed, 3), uptime, client.me.mention)
    if img:
        img = random.choice(img.split(" "))
        await message.reply_document(
            img,
            caption=caption,
            force_document=False,
        )
        return
    await hellbot.edit(hell, caption, no_link_preview=True)


HelpMenu("bot").add("alive", None, "Get the alive message of the bot.", "alive").add(
    "ping",
    None,
    "Check the ping speed and uptime of bot.",
    "ping",
    "You can also customize ping message by adding a media to it.",
).info("Alive Menu").done()
