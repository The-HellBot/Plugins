import os
import time
import zipfile

from pyrogram.types import Message

from Hellbot.functions.formatter import readable_time
from Hellbot.functions.tools import get_files_from_directory, progress

from . import Config, HelpMenu, hellbot, on_message


@on_message("zip", allow_stan=True)
async def zip_files(_, message: Message):
    if not message.reply_to_message:
        return await hellbot.delete(message, "Reply to a message to zip it.")

    media = message.reply_to_message.media
    if not media:
        return await hellbot.delete(message, "Reply to a media message to zip it.")

    hell = await hellbot.edit(message, "`Zipping...`")
    start = time.time()
    download_path = await message.reply_to_message.download(
        f"{Config.TEMP_DIR}temp_{round(time.time())}",
        progress=progress,
        progress_args=(hell, start, "📦 Zipping"),
    )

    zip_path = Config.TEMP_DIR + f"zipped_{int(time.time())}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write(download_path)

    await hellbot.delete(hell, "Zipped Successfully.")
    await message.reply_document(
        zip_path,
        caption=f"**Zipped in {readable_time(time.time() - start)}.**",
        progress=progress,
        progress_args=(hell, start, "⬆️ Uploading"),
    )

    os.remove(zip_path)
    os.remove(download_path)


@on_message("unzip", allow_stan=True)
async def unzip_file(_, message: Message):
    if not message.reply_to_message:
        return await hellbot.delete(message, "Reply to a message to unzip it.")

    media = message.reply_to_message.media
    if not media:
        return await hellbot.delete(message, "Reply to a media message to unzip it.")

    hell = await hellbot.edit(message, "`Unzipping...`")
    start = time.time()
    download_path = await message.reply_to_message.download(
        f"{Config.TEMP_DIR}temp_{round(time.time())}",
        progress=progress,
        progress_args=(hell, start, "📦 Unzipping"),
    )

    with zipfile.ZipFile(download_path, "r") as zip_file:
        if not os.path.isdir(Config.TEMP_DIR + "unzipped/"):
            os.mkdir(Config.TEMP_DIR + "unzipped/")
        zip_file.extractall(Config.TEMP_DIR + "unzipped/")

    await hellbot.delete(hell, "Unzipped Successfully.")
    files = await get_files_from_directory(Config.TEMP_DIR + "unzipped/")

    for file in files:
        if os.path.exists(file):
            try:
                await message.reply_document(
                    file,
                    caption=f"**Unzipped {os.path.basename(file)}.**",
                    force_document=True,
                    progress=progress,
                    progress_args=(hell, start, "⬆️ Uploading"),
                )
            except Exception as e:
                await message.reply_text(f"**{file}:** `{e}`")
                continue
            os.remove(file)

    os.remove(download_path)


HelpMenu("archiver").add(
    "zip",
    "<reply to a media>",
    "Zip the replied media and upload it in the chat.",
).add(
    "unzip",
    "<reply to a zip file>",
    "Unzip the replied zip file and upload it in the chat.",
).info(
    "Manage Archives"
).done()
