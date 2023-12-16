import os
from shutil import rmtree

from glitch_this import ImageGlitcher
from PIL import Image
from pyrogram.enums import MessageMediaType
from pyrogram.types import InputMediaPhoto, Message

from Hellbot.core import ENV
from Hellbot.functions.google import googleimagesdownload
from Hellbot.functions.images import get_wallpapers
from Hellbot.functions.tools import runcmd

from . import Config, HelpMenu, db, hellbot, on_message


@on_message(["image", "img"], allow_stan=True)
async def searchImage(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(message, "Provide a search query.")

    limit = 5
    query = await hellbot.input(message)
    hell = await hellbot.edit(message, "Searching...")

    if ";" in query:
        try:
            query, limit = query.split(";", 1)
            limit = int(limit)
        except:
            pass

    googleImage = googleimagesdownload()
    to_send = []
    args = {
        "keywords": query,
        "limit": limit,
        "format": "jpg",
        "output_directory": Config.DWL_DIR,
    }

    path_args, _ = googleImage.download(args)
    images = path_args.get(query)
    for image in images:
        to_send.append(InputMediaPhoto(image))

    if to_send:
        await hell.reply_media_group(to_send)
        await hellbot.delete(hell, "Uploaded!")
    else:
        await hellbot.delete(hell, "No images found.")

    try:
        rmtree(Config.DWL_DIR + query + "/")
    except:
        pass


@on_message("wallpaper", allow_stan=True)
async def searchWallpaper(_, message: Message):
    if len(message.command) < 2:
        random = True
        query = ""
    else:
        random = False
        query = await hellbot.input(message)

    to_send = []
    limit = 10
    hell = await hellbot.edit(message, "Processing...")

    access = await db.get_env(ENV.unsplash_api)
    if not access:
        return await hellbot.delete(hell, "Unsplash API not found.")

    if ";" in query:
        try:
            query, limit = query.split(";", 1)
            limit = int(limit)
        except:
            pass

    if limit > 30:
        return await hellbot.delete(hell, "Limit should be less than 30.")
    elif limit < 1:
        return await hellbot.delete(hell, "Limit should be greater than 0.")

    wallpapers = await get_wallpapers(access, limit, query, random)
    if not wallpapers:
        return await hellbot.delete(hell, "No wallpapers found.")

    for wallpaper in wallpapers:
        to_send.append(InputMediaPhoto(wallpaper))

    await hell.reply_media_group(to_send)
    await hellbot.delete(hell, "Uploaded!")


@on_message("glitch", allow_stan=True)
async def glitcher(_, message: Message):
    if not message.reply_to_message or not message.reply_to_message.media:
        return await hellbot.delete(message, "Reply to a media message to glitch it.")

    hell = await hellbot.edit(message, "Glitching...")
    media = message.reply_to_message.media

    intensity = 2
    if len(message.command) > 1:
        intensity = int(message.command[1]) if message.command[1].isdigit() else 2

    if not 0 < intensity < 9:
        await hell.edit("intensity should be between 1 and 8... now glitching at 8")

    if media and media not in [
        MessageMediaType.ANIMATION,
        MessageMediaType.VIDEO,
        MessageMediaType.PHOTO,
        MessageMediaType.STICKER,
    ]:
        return await hellbot.delete(hell, "Only media messages are supported.")

    glitch_img = os.path.join(Config.TEMP_DIR, "glitch.png")
    dwl_path = await message.reply_to_message.download(Config.DWL_DIR)

    if dwl_path.endswith(".tgs"):
        cmd = f"lottie_convert.py --frame 0 -if lottie -of png {dwl_path} {glitch_img}"
        stdout, stderr, _, _ = await runcmd(cmd)
        if not os.path.lexists(glitch_img):
            return await hellbot.error(hell, f"`{stdout}`\n`{stderr}`")
    elif dwl_path.endswith(".webp"):
        os.rename(dwl_path, glitch_img)
        if not os.path.lexists(glitch_img):
            return await hellbot.error(hell, "File not found.")
    elif media in [MessageMediaType.VIDEO, MessageMediaType.ANIMATION]:
        cmd = f"ffmpeg -ss 0 -i {dwl_path} -vframes 1 {glitch_img}"
        stdout, stderr, _, _ = await runcmd(cmd)
        if not os.path.lexists(glitch_img):
            return await hellbot.error(hell, f"`{stdout}`\n`{stderr}`")
    else:
        os.rename(dwl_path, glitch_img)
        if not os.path.lexists(glitch_img):
            return await hellbot.error(hell, "File not found.")

    glitcher = ImageGlitcher()
    img = Image.open(glitch_img)
    glitch = glitcher.glitch_image(img, intensity, color_offset=True, gif=True)

    output_path = os.path.join(Config.TEMP_DIR, "glitch.gif")
    glitch[0].save(
        fp=output_path,
        format="GIF",
        append_images=glitch[1:],
        save_all=True,
        duration=200,
        loop=0,
    )

    await message.reply_animation(output_path)
    await hellbot.delete(hell, f"Glitched at intensity {intensity}")
    os.remove(output_path)
    os.remove(glitch_img)
    try:
        os.remove(dwl_path)
    except BaseException:
        pass


HelpMenu("images").add(
    "image",
    "<query> ; <limit>",
    "Search for x images on google and upload them to current chat,",
    "image hellbot ; 5",
    "An alias of 'img' can also be used.",
).add(
    "wallpaper",
    "<query> ; <limit>",
    "Search for x wallpapers on unsplash and upload them to current chat. Requires unsplash API.",
    "wallpaper supra ; 5",
    "If no query is given, random wallpapers will be uploaded.",
).add(
    "glitch",
    "<reply to media>",
    "Glitch a media message. It includes sticker, gif, photo, video.",
    "glitch 4",
).info(
    "Image Tools"
).done()
