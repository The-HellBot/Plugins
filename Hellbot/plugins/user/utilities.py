import os

from pyrogram import Client
from pyrogram.types import Message

from Hellbot.core import ENV
from Hellbot.functions.media import get_media_text_ocr
from Hellbot.functions.paste import spaceBin

from . import Config, HelpMenu, db, hellbot, on_message


@on_message("readimage", allow_stan=True)
async def readImage(_, message: Message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await hellbot.delete(message, "Reply to a photo to read text on it.")

    api_key = await db.get_env(ENV.ocr_api)
    if not api_key:
        return await hellbot.delete(
            message, "To read texts from images you need to setup OCR Space Api key."
        )

    language = "eng"
    if len(message.command) >= 2:
        language = message.command[1]

    hell = await hellbot.edit(message, "Reading image...")

    filename = await message.reply_to_message.download(Config.TEMP_DIR)
    text = await get_media_text_ocr(filename, api_key, language)

    try:
        await hellbot.edit(hell, text["ParsedResults"][0]["ParsedText"])
    except Exception as e:
        await hellbot.error(hell, f"`{e}`")

    os.remove(filename)


@on_message("paste", allow_stan=True)
async def paste_text(_, message: Message):
    if (
        len(message.command) < 2
        or not message.reply_to_message
        or not message.reply_to_message.text
        or not message.reply_to_message.document
    ):
        return await hellbot.delete(message, "Reply to a text to paste it.")

    hell = await hellbot.edit(message, "Pasting text...")

    text_to_paste = ""
    extention = "none"
    if len(message.command) >= 2:
        text_to_paste = await hellbot.input(message)
    elif message.reply_to_message.text:
        text_to_paste = message.reply_to_message.text
    elif message.reply_to_message.document:
        filename = await message.reply_to_message.download(Config.TEMP_DIR)
        with open(filename, "r") as f:
            text_to_paste = f.read()
        extention = filename.split(".")[-1]
        os.remove(filename)
    else:
        return await hellbot.delete(message, "Reply to a text to paste it.")

    try:
        paste_link = spaceBin(text_to_paste, extention)

        await hell.edit(
            f"**📝 Pasted to:** {paste_link}",
            disable_web_page_preview=True,
        )
    except Exception as e:
        await hellbot.error(hell, f"`{e}`")


HelpMenu("utilities").add(
    "readimage",
    "<reply to message> <language code (optional)>",
    "Read the texts on the image and send it as a message.",
    "read eng",
).add(
    "paste",
    "<reply to message> or <text>",
    "Paste the text to spaceb.in and send the link.",
    "paste",
).info(
    "Some utilities command!"
).done()
