import os
import time

from PIL import Image
from pyrogram.enums import MessageMediaType
from pyrogram.types import Message

from Hellbot.functions.convert import tgs_to_png, video_to_png
from Hellbot.functions.images import draw_meme
from Hellbot.functions.media import get_metedata
from Hellbot.functions.paste import post_to_telegraph
from Hellbot.functions.tools import progress, runcmd

from . import Config, HelpMenu, hellbot, on_message


@on_message("mediainfo", allow_stan=True)
async def mediaInfo(_, message: Message):
    if not message.reply_to_message or not message.reply_to_message.media:
        return await hellbot.delete(message, "Reply to a media file")

    media = message.reply_to_message.media
    hell = await hellbot.edit(message, "Getting media info...")

    if media == MessageMediaType.ANIMATION:
        media_file = message.reply_to_message.animation
    elif media == MessageMediaType.AUDIO:
        media_file = message.reply_to_message.audio
    elif media == MessageMediaType.DOCUMENT:
        media_file = message.reply_to_message.document
    elif media == MessageMediaType.PHOTO:
        media_file = message.reply_to_message.photo
    elif media == MessageMediaType.STICKER:
        media_file = message.reply_to_message.sticker
    elif media == MessageMediaType.VIDEO:
        media_file = message.reply_to_message.video
    else:
        return await hellbot.delete(message, "Unsupported media type")

    metadata = await get_metedata(media_file)
    if not metadata:
        return await hellbot.delete(message, "Failed to get media info")

    await hell.edit(f"Fetched metadata, now fetching extra mediainfo...")

    start_time = time.time()
    try:
        file_path = await message.reply_to_message.download(
            Config.DWL_DIR,
            progress=progress,
            progress_args=(hell, start_time, "⬇️ Downloading"),
        )
    except Exception as e:
        return await hell.edit(
            f"**Failed to download media check the metadata instead!**\n\n{metadata}"
        )

    out, _, _, _ = await runcmd(f"mediainfo '{file_path}'")
    if not out:
        return await hell.edit(
            f"Failed to get mediainfo, check the metadata instead!\n\n{metadata}"
        )

    await hell.edit(f"Uploading mediainfo to telegraph...")

    to_paste = f"<h1>💫 HellBot Media Info:</h1><br>{metadata}<br><b>📝 MediaInfo:</b><br><code>{out}</code>"
    link = await post_to_telegraph("HellBotMediaInfo", to_paste)

    await hell.edit(f"**📌 Media Info:** [Here]({link})")
    os.remove(file_path)


@on_message(["mmf", "memify"], allow_stan=True)
async def memify(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(message, "Enter some text!")

    if not message.reply_to_message or not message.reply_to_message.media:
        return await hellbot.delete(message, "Reply to a media file")

    start_time = time.time()
    hell = await hellbot.edit(message, "Memifying...")
    file = await message.reply_to_message.download(
        Config.DWL_DIR,
        progress=progress,
        progress_args=(hell, start_time, "⬇️ Downloading"),
    )

    text = await hellbot.input(message)
    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text, lower_text = text, ""

    if file and file.endswith(".tgs"):
        await hell.edit("Looks like an animated sticker, converting to image...")
        pic = await tgs_to_png(file)
    elif file and file.endswith((".webp", ".png")):
        pic = Image.open(file).save(file, "PNG", optimize=True)
    elif file:
        await hell.edit("Converting to image...")
        pic, status = await video_to_png(file, 0)
        if status == False:
            return await hellbot.error(hell, pic)
    else:
        return await hellbot.delete(message, "Unsupported media type")

    await hell.edit("Adding text...")
    memes = await draw_meme(file, upper_text, lower_text)

    await hell.edit("Done!")
    await message.reply_sticker(memes[1])
    await message.reply_photo(
        memes[0],
        caption=f"**🍀 𝖬𝖾𝗆𝗂𝖿𝗂𝖾𝖽 𝗎𝗌𝗂𝗇𝗀 𝖧𝖾𝗅𝗅𝖡𝗈𝗍!**",
    )

    os.remove(pic)
    os.remove(file)
    os.remove(memes[0])
    os.remove(memes[1])


HelpMenu("media").add(
    "mediainfo",
    "<reply to media message>",
    "Get the metadata and detailed media info of replied media file.",
    "mediainfo",
).add(
    "memify",
    "<reply to media message> <upper text>;<lower text>",
    "Add text to a media file and make it a meme.",
    "memify Hello World",
    "When ';' is used, the text before it will be the upper text and the text after it will be the lower text.",
).info(
    "Mediainfo & Media Edits"
).done()
