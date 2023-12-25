import os
import uuid

from pyrogram import Client
from pyrogram.enums import MessageMediaType
from pyrogram.types import Message

from Hellbot.functions.images import convert_to_png
from Hellbot.functions.utility import TGraph

from . import Config, HelpMenu, Symbols, hellbot, on_message


@on_message(["tgm", "tm"], allow_stan=True)
async def telegraph_media(_, message: Message):
    if not message.reply_to_message or not message.reply_to_message.media:
        return await hellbot.edit(message, "__Reply to a media message!__")

    hell = await hellbot.edit(message, "__Uploading to telegraph...__")

    if message.reply_to_message.media in [
        MessageMediaType.ANIMATION,
        MessageMediaType.VIDEO,
    ]:
        file_size = (
            message.reply_to_message.animation.file_size
            if message.reply_to_message.animation
            else message.reply_to_message.video.file_size
        )

        if file_size >= 5242880:
            return await hellbot.delete(
                hell,
                "__This media is too big to upload to telegraph! You need to choose media below 5mb.__",
            )

        path = await message.reply_to_message.download(Config.TEMP_DIR)

    elif message.reply_to_message.media in [
        MessageMediaType.PHOTO,
        MessageMediaType.STICKER,
        MessageMediaType.DOCUMENT,
    ]:
        file_size = (
            message.reply_to_message.photo.file_size
            if message.reply_to_message.photo
            else message.reply_to_message.sticker.file_size
            if message.reply_to_message.sticker
            else message.reply_to_message.document.file_size
        )

        if file_size >= 5242880:
            return await hellbot.delete(
                hell,
                "__This media is too big to upload to telegraph! You need to choose media below 5mb.__",
            )

        if message.reply_to_message.document:
            if message.reply_to_message.document.mime_type.lower().split("/")[0] in [
                "image",
                "video",
            ]:
                path = await message.reply_to_message.download(Config.TEMP_DIR)
            else:
                return await hellbot.delete(hell, "This media is not supported!")
        else:
            path = await message.reply_to_message.download(Config.TEMP_DIR)
    else:
        return await hellbot.delete(hell, "This media is not supported!")

    if path.lower().endswith(".webp"):
        path = convert_to_png(path)

    await hell.edit(
        f"**Media downloaded to local server.** __Now uploading to telegraph...__"
    )

    try:
        media_url = TGraph.telegraph.upload_file(path)
        url = f"https://te.legra.ph{media_url[0]['src']}"
    except Exception as e:
        await hellbot.error(hell, str(e))
    else:
        await hell.edit(
            f"**💫 Uploaded to [telegraph]({url})!**\n\n**{Symbols.anchor} URL:** `{url}`",
            disable_web_page_preview=True,
        )

    os.remove(path)


@on_message(["tgt", "tt"], allow_stan=True)
async def telegraph_text(client: Client, message: Message):
    if len(message.command) < 2:
        page_name = client.me.first_name
    else:
        page_name = await hellbot.input(message)

    if not message.reply_to_message:
        return await hellbot.edit(
            message, "__Reply to a message to upload it on telegraph page!__"
        )

    hell = await hellbot.edit(message, "__Uploading to telegraph...__")

    page_content = (
        message.reply_to_message.text or message.reply_to_message.caption or ""
    )

    media_list = None
    if message.reply_to_message.media:
        page_media = await message.reply_to_message.download(Config.TEMP_DIR)

        with open(page_media, "rb") as f:
            media_list = f.readlines()

        for media in media_list:
            page_content += media.decode("utf-8") + "\n"

        os.remove(page_media)

    page_content = page_content.replace("\n", "<br>")

    try:
        response = TGraph.telegraph.create_page(page_name, html_content=page_content)
    except Exception:
        rnd_key = uuid.uuid4().hex[:8]
        page_name = f"{page_name}_{rnd_key}"
        response = TGraph.telegraph.create_page(page_name, html_content=page_content)

    try:
        url = f"https://te.legra.ph/{response['path']}"
        await hell.edit(
            f"**💫 Uploaded to [telegraph]({url})!**\n\n**{Symbols.anchor} URL:** `{url}`",
            disable_web_page_preview=True,
        )
    except Exception as e:
        await hellbot.error(hell, str(e))


HelpMenu("telegraph").add(
    "tgm",
    "<reply to media>",
    "Upload the replied media message to telegra.ph and returns a direct url.",
    "tgm",
    "An alias of 'tm' is also available.",
).add(
    "tgt",
    "<reply to message> <page title>",
    "Upload the replied message content to telegra.ph!",
    "tgt",
    "An alias of 'tt' is also available.",
).info(
    "Telegraph Uploader"
).done()
