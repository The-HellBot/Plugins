import io
import os
from shutil import rmtree
import time
import requests
from glitch_this import ImageGlitcher
from PIL import Image
from pyrogram.enums import MessageMediaType
from pyrogram.types import InputMediaPhoto, Message, InputMediaDocument

from Hellbot.core import ENV
from Hellbot.functions.google import googleimagesdownload
from Hellbot.functions.images import get_wallpapers, deep_fry
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

    trash = []
    for i, wallpaper in enumerate(wallpapers):
        file_name = f"{i}_{int(time.time())}.jpg"
        with open(file_name, "wb") as f:
            f.write(requests.get(wallpaper).content)
        to_send.append(InputMediaDocument(file_name))
        trash.append(file_name)

    await hell.reply_media_group(to_send)
    await hellbot.delete(hell, "Uploaded!")
    [os.remove(trash_file) for trash_file in trash]


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


@on_message("deepfry", allow_stan=True)
async def deepfry(_, message: Message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await hellbot.delete(message, "Reply to a photo to deepfry it.")

    if len(message.command) > 1:
        try:
            quality = int(message.command[1])
        except ValueError:
            quality = 2
    else:
        quality = 2

    hell = await hellbot.edit(message, "Deepfrying...")
    photo = await message.reply_to_message.download(Config.DWL_DIR)

    if quality > 9:
        quality = 9
    elif quality < 1:
        quality = 2

    image = Image.open(photo)
    for _ in range(quality):
        image = await deep_fry(image)

    fried = io.BytesIO()
    fried.name = "deepfried.jpeg"
    image.save(fried, "JPEG")
    fried.seek(0)

    await hell.reply_photo(fried)
    await hellbot.delete(hell, "Deepfried!")

    os.remove(photo)


HelpMenu("images").add(
    "image",
    "<query> ; <limit>",
    "Search for x images on google and upload them to current chat,",
    "image hellbot ; 5",
    "An alias of 'img' can also be used.",
).add(
    "wallpaper",
    "<query> ; <limit>",
    "Search for x wallpapers on unsplash and upload them to current chat. If no query is given, random wallpapers will be uploaded.",
    "wallpaper supra ; 5",
    "Need to setup Unsplash Api key from https://unsplash.com/join",
).add(
    "glitch",
    "<reply to media> <intensity>",
    "Glitch a media message. It includes sticker, gif, photo, video. The intensity can be changed by passing an integer between 1 and 8. Default is 2.",
    "glitch 4",
).add(
    "deepfry",
    "<reply to photo> <quality>",
    "Deepfry a photo. The quality can be changed by passing an integer between 1 and 9. Default is 2.",
    "deepfry 5",
).info(
    "Image Tools"
).done()
