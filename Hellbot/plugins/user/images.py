import os

from glitch_this import ImageGlitcher
from PIL import Image
from pyrogram.enums import MessageMediaType
from pyrogram.types import Message

from Hellbot.functions.tools import runcmd

from . import Config, HelpMenu, hellbot, on_message


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
    "glitch",
    "<reply to media>",
    "Glitch a media message. It includes sticker, gif, photo, video.",
    "glitch 4",
).info("Image Tools").done()
