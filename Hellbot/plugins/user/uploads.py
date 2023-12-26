import os
import time

from pyrogram import Client
from pyrogram.types import Message

from Hellbot.functions.formatter import readable_time
from Hellbot.functions.tools import progress

from . import HelpMenu, db, hellbot, on_message


@on_message("upload", allow_stan=True)
async def uploadfiles(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(message, "Provide a valid file path.")

    query = await hellbot.input(message)
    hell = await hellbot.edit(message, f"**Uploading...** `{query}`")

    if not os.path.exists(query):
        return await hellbot.error(hell, f"**Error:** `{query}` **not found.**")

    try:
        ul_start = time.time()
        await message.reply_document(
            query,
            progress=progress,
            progress_args=(hell, ul_start, f"**Uploading...** `{query}`"),
        )
        ul_time = readable_time(int(time.time() - ul_start))
        await hellbot.delete(hell, f"**Uploaded** `{query}` **in** `{ul_time}`")
    except Exception as e:
        return await hellbot.error(hell, f"**Error:** `{e}`")


@on_message("uploaddir", allow_stan=True)
async def uploadDir(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(message, "Provide a valid directory path.")

    query = await hellbot.input(message)
    hell = await hellbot.edit(message, f"**Uploading...** `{query}`")

    if not os.path.exists(query):
        return await hellbot.error(hell, f"**Error:** `{query}` **not found.**")

    files_list = []
    for root, dirs, files in os.walk(query):
        for file in files:
            files_list.append(os.path.join(root, file))
        for dir in dirs:
            files_list.append(os.path.join(root, dir))

    uploaded = 0
    await hell.edit(f"**Uploading...** `{len(files_list)} files...`")

    ul_start = time.time()
    for file in files_list:
        try:
            ul_start_file = time.time()
            await message.reply_document(
                file,
                caption=f"**📂 File:** `{os.path.basename(file)}`",
                progress=progress,
                progress_args=(hell, ul_start_file, f"**Uploading...** `{file}`"),
            )
            uploaded += 1
        except Exception:
            continue

    ul_time = readable_time(int(time.time() - ul_start))
    await hell.edit(
        f"**Uploaded** `{uploaded}/{len(files_list)}` **files in** `{ul_time}`"
    )


HelpMenu("uploads").add(
    "upload",
    "<filepath>",
    "Uploads the mentioned file from the local server to current chat.",
    "upload README.md",
    "Be cautious while uploading files.",
).add(
    "uploaddir",
    "<dirpath>",
    "Uploads all the files from the mentioned directory to current chat.",
    "uploaddir ./downloads/",
    "Be cautious while uploading files.",
).info(
    "Upload Manager"
).done()
