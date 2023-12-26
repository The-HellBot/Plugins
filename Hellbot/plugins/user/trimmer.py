import os
import time

from pyrogram.types import Message

from Hellbot.functions.formatter import readable_time
from Hellbot.functions.tools import progress, runcmd

from . import Config, HelpMenu, hellbot, on_message


@on_message("vtrim", allow_stan=True)
async def videotrim(_, message: Message):
    if message.reply_to_message:
        if not (message.reply_to_message.video or message.reply_to_message.document):
            return await hellbot.delete(message, "Reply to a video file")

    if len(message.command) < 2:
        return await hellbot.delete(message, "Provide a valid timestamp.")

    if message.reply_to_message.document:
        if message.reply_to_message.document.mime_type.lower().split("/")[0] not in [
            "video",
        ]:
            return await hellbot.delete(message, "Reply to a video file")

    start = message.command[1].strip()
    end = None
    if len(message.command) > 2:
        end = message.command[2].strip()

    dl_start = time.time()
    hell = await hellbot.edit(message, "Downloading...")
    file = await message.reply_to_message.download(
        Config.DWL_DIR,
        progress=progress,
        progress_args=(hell, dl_start, "⬇️ Downloading..."),
    )

    dl_time = readable_time(int(time.time() - dl_start))
    await hell.edit(f"**Downloaded in {dl_time}!** __Starting to trim video...__")

    if end:
        file_name = os.path.join(Config.TEMP_DIR, f"trim_{int(time.time())}.mp4")
        cmd = f"ffmpeg -i {file} -ss {start} -to {end} -async 1 -strict -2 {file_name}"
        caption = f"**Trimmed {start} to {end}!**\n\n**Trimmed By:** {message.from_user.mention}"
    else:
        file_name = os.path.join(Config.TEMP_DIR, f"trim_{int(time.time())}.jpg")
        cmd = f"ffmpeg -i {file} -ss {start} -vframes 1 {file_name}"
        caption = f"**Trimmed {start}!**\n\n**Trimmed By:** {message.from_user.mention}"

    _, err, _, _ = await runcmd(cmd)
    if not os.path.lexists(file_name):
        return await hellbot.error(hell, f"**Error:** `{err}`")

    ul_start = time.time()
    await hell.edit("**Trimmed!** __Uploading now...__")
    await message.reply_document(
        file_name,
        caption=caption,
        progress=progress,
        progress_args=(hell, ul_start, "**Trimmed!** __Uploading now...__"),
    )

    await hellbot.delete(
        hell,
        f"**Trimmed!** __Uploaded in {readable_time(int(time.time() - ul_start))}!__",
    )

    os.remove(file)
    os.remove(file_name)


@on_message("atrim", allow_stan=True)
async def audiotrim(_, message: Message):
    if message.reply_to_message:
        if not (message.reply_to_message.video or message.reply_to_message.document or message.reply_to_message.audio):
            return await hellbot.delete(message, "Reply to a video/audio file")

    if len(message.command) < 3:
        return await hellbot.delete(message, "Provide a valid timestamp.")

    if message.reply_to_message.document:
        if message.reply_to_message.document.mime_type.lower().split("/")[0] not in [
            "audio",
            "video",
        ]:
            return await hellbot.delete(message, "Reply to a video/audio file")

    start = message.command[1].strip()
    end = message.command[2].strip()

    dl_start = time.time()
    hell = await hellbot.edit(message, "Downloading...")
    file = await message.reply_to_message.download(
        Config.DWL_DIR,
        progress=progress,
        progress_args=(hell, dl_start, "⬇️ Downloading..."),
    )

    dl_time = readable_time(int(time.time() - dl_start))
    await hell.edit(f"**Downloaded in {dl_time}!** __Starting to trim audio...__")

    file_name = os.path.join(Config.TEMP_DIR, f"trim_{int(time.time())}.mp3")
    cmd = f"ffmpeg -i {file} -ss {start} -to {end} -async 1 -strict -2 {file_name}"
    caption = (
        f"**Trimmed {start} to {end}!**\n\n**Trimmed By:** {message.from_user.mention}"
    )

    out, err, _, _ = await runcmd(cmd)
    if not os.path.lexists(file_name):
        return await hellbot.error(hell, f"**Error:** `{err}`")

    ul_start = time.time()
    await hell.edit("**Trimmed!** __Uploading now...__")
    await message.reply_audio(
        file_name,
        caption=caption,
        progress=progress,
        progress_args=(hell, ul_start, "**Trimmed!** __Uploading now...__"),
    )

    await hellbot.delete(
        hell,
        f"**Trimmed!** __Uploaded in {readable_time(int(time.time() - ul_start))}!__",
    )

    os.remove(file)
    os.remove(file_name)


HelpMenu("trimmer").add(
    "vtrim",
    "<start> <end (optional)>",
    "Trim a video from <start> to <end>.",
    "vtrim 2:39 3:00",
    "If only one timestamp is provided, it will take a screenshot of that frame.",
).add(
    "atrim",
    "<start> <end>",
    "Trim an audio from <start> to <end>.",
    "atrim 2:39 3:00",
    "Start and end time must be provided.",
).info(
    "Trim Audio & Video"
).done()
