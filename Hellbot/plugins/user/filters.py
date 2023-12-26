import asyncio
import re

from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.types import Message

from . import HelpMenu, custom_handler, db, handler, hellbot, on_message


@on_message("filter", allow_stan=True)
async def set_filter(client: Client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await hellbot.delete(
            message, f"Reply to a message with {handler}filter <keyword> to save it as a filter."
        )

    keyword = await hellbot.input(message)
    replied = message.reply_to_message

    hell = await hellbot.edit(message, f"Saving filter `{keyword}`")

    if replied.media:
        if replied.media == MessageMediaType.ANIMATION:
            file_id = replied.animation.file_id
            caption = replied.caption
        elif replied.media == MessageMediaType.AUDIO:
            file_id = replied.audio.file_id
            caption = replied.caption
        elif replied.media == MessageMediaType.DOCUMENT:
            file_id = replied.document.file_id
            caption = replied.caption
        elif replied.media == MessageMediaType.PHOTO:
            file_id = replied.photo.file_id
            caption = replied.caption
        elif replied.media == MessageMediaType.VIDEO:
            file_id = replied.video.file_id
            caption = replied.caption
        elif replied.media == MessageMediaType.VIDEO_NOTE:
            file_id = replied.video_note.file_id
            caption = replied.caption
        elif replied.media == MessageMediaType.VOICE:
            file_id = replied.voice.file_id
            caption = replied.caption
        elif replied.media == MessageMediaType.STICKER:
            file_id = replied.sticker.file_id
            caption = replied.caption
        else:
            return await hellbot.delete(hell, "This media type is not supported.")
    else:
        file_id = None
        caption = replied.text or replied.caption

    await db.set_filter(
        client.me.id, message.chat.id, keyword.lower(), file_id, caption
    )
    await hellbot.delete(hell, f"**🍀 𝖭𝖾𝗐 𝖥𝗂𝗅𝗍𝖾𝗋 𝖲𝖺𝗏𝖾𝖽:** `{keyword}`")


@on_message(["rmfilter", "rmallfilter"], allow_stan=True)
async def rmfilter(client: Client, message: Message):
    if len(message.command[0]) < 9:
        if len(message.command) < 2:
            return await hellbot.delete(message, "Give a filter name to remove.")

        keyword = await hellbot.input(message)
        hell = await hellbot.edit(message, f"Removing filter `{keyword}`")

        if await db.is_filter(client.me.id, message.chat.id, keyword.lower()):
            await db.rm_filter(client.me.id, message.chat.id, keyword.lower())
            await hellbot.delete(hell, f"**🍀 𝖥𝗂𝗅𝗍𝖾𝗋 𝖱𝖾𝗆𝗈𝗏𝖾𝖽:** `{keyword}`")
        else:
            await hellbot.delete(hell, f"**🍀 𝖥𝗂𝗅𝗍𝖾𝗋 𝖽𝗈𝖾𝗌 𝗇𝗈𝗍 𝖾𝗑𝗂𝗌𝗍𝗌:** `{keyword}`")
    else:
        hell = await hellbot.edit(message, "Removing all filters...")

        await db.rm_all_filters(client.me.id, message.chat.id)
        await hellbot.delete(hell, "All filters have been removed.")


@on_message(["getfilter", "getfilters"], allow_stan=True)
async def allfilters(client: Client, message: Message):
    if len(message.command) > 1:
        keyword = await hellbot.input(message)
        hell = await hellbot.edit(message, f"Getting filter `{keyword}`")

        if await db.is_filter(client.me.id, message.chat.id, keyword.lower()):
            data = await db.get_filter(client.me.id, message.chat.id, keyword.lower())
            data = data["filter"][0]

            file_id = data.get("fileId", None)
            caption = data.get("text", None)

            if file_id:
                sent = await message.reply_cached_media(file_id, caption=caption)
                await sent.reply_text(f"**🍀 𝖥𝗂𝗅𝗍𝖾𝗋:** `{keyword}`")
                await hell.delete()

            else:
                await hell.edit(f"**🍀 𝖥𝗂𝗅𝗍𝖾𝗋:** `{keyword}`\n\n{caption}")

        else:
            await hellbot.delete(hell, f"**🍀 𝖥𝗂𝗅𝗍𝖾𝗋 𝖽𝗈𝖾𝗌 𝗇𝗈𝗍 𝖾𝗑𝗂𝗌𝗍𝗌:** `{keyword}`")

    else:
        hell = await hellbot.edit(message, "Getting all filters...")
        filters = await db.get_all_filters(client.me.id, message.chat.id)

        if filters:
            text = f"**🍀 𝖭𝗈. 𝗈𝖿 𝖥𝗂𝗅𝗍𝖾𝗋𝗌 𝗂𝗇 𝗍𝗁𝗂𝗌 𝖼𝗁𝖺𝗍:** `{len(filters)}`\n\n"

            for i, filter in enumerate(filters, 1):
                text += f"** {'0' if i < 10 else ''}{i}:** `{filter['keyword']}`\n"

            await hell.edit(text)

        else:
            await hellbot.delete(hell, "No filters in this chat.")


@custom_handler(filters.incoming)
async def handle_filters(client: Client, message: Message):
    data = await db.get_all_filters(client.me.id, message.chat.id)
    if not data:
        return

    msg = message.text or message.caption
    if not msg:
        return

    for filter in data:
        pattern = r"( |^|[^\w])" + re.escape(filter["keyword"]) + r"( |$|[^\w])"
        if re.search(pattern, msg, flags=re.IGNORECASE):
            file_id = filter.get("fileId", None)
            caption = filter.get("text", None)

            if file_id:
                await message.reply_cached_media(file_id, caption=caption)
            else:
                await message.reply_text(caption)
            await asyncio.sleep(1)


HelpMenu("filters").add(
    "filter",
    "<keyword> <reply to a message>",
    "Saves the replied message as a filter to given keyword along the command.",
    "filter hellbot",
    "You need to reply to the message you want to save as filter. You can also save media as filters alonng with captions.",
).add(
    "rmfilter",
    "<keyword>",
    "Removes the filter with given keyword.",
    "rmfilter hellbot",
).add(
    "rmallfilter",
    None,
    "Removes all the filters in current chat.",
    "rmallfilter",
).add(
    "getfilter",
    "<keyword>",
    "Gives the filter data associated with given keyword.",
    "getfilter hellbot",
).add(
    "getfilters", None, "Gets all filters in the chat.", "getfilters"
).info(
    "Filter Module"
).done()
