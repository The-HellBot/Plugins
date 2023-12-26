from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.types import Message

from . import HelpMenu, custom_handler, db, handler, hellbot, on_message


@on_message(["snip", "note"], allow_stan=True)
async def addsnip(client: Client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await hellbot.delete(
            message,
            f"Reply to a message with {handler}snip <keyword> to save it as a snip.",
        )

    keyword = await hellbot.input(message)
    replied = message.reply_to_message

    hell = await hellbot.edit(message, f"Saving snip `#{keyword}`")
    replied = message.reply_to_message

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

    await db.set_snip(client.me.id, message.chat.id, keyword.lower(), file_id, caption)

    await hellbot.delete(hell, f"**📌 𝖭𝖾𝗐 𝖲𝗇𝗂𝗉 𝖭𝗈𝗍𝖾 𝖲𝖺𝗏𝖾𝖽:** `#{keyword}`")


@on_message(["rmsnip", "rmallsnip"], allow_stan=True)
async def rmsnip(client: Client, message: Message):
    if len(message.command[0]) < 7:
        if len(message.command) < 2:
            return await hellbot.delete(message, "Give a snip note name to remove.")

        keyword = await hellbot.input(message)
        hell = await hellbot.edit(message, f"Removing snip `#{keyword}`")

        if await db.is_snip(client.me.id, message.chat.id, keyword.lower()):
            await db.rm_snip(client.me.id, message.chat.id, keyword.lower())
            await hellbot.delete(hell, f"**🍀 𝖲𝗇𝗂𝗉 𝖭𝗈𝗍𝖾 𝖱𝖾𝗆𝗈𝗏𝖾𝖽:** `#{keyword}`")
        else:
            await hellbot.delete(hell, f"**🍀 𝖲𝗇𝗂𝗉 𝖭𝗈𝗍𝖾 𝖽𝗈𝖾𝗌 𝗇𝗈𝗍 𝖾𝗑𝗂𝗌𝗍𝗌:** `#{keyword}`")
    else:
        hell = await hellbot.edit(message, "Removing all filters...")
        await db.rm_all_snips(client.me.id, message.chat.id)
        await hellbot.delete(hell, "All snips have been removed.")


@on_message(["getsnip", "snips"], allow_stan=True)
async def snips(client: Client, message: Message):
    if message.command[0][0] == "g":
        if len(message.command) < 2:
            return await hellbot.delete(message, "Give a snip note name to get.")
        keyword = await hellbot.input(message)
        hell = await hellbot.edit(message, f"Getting snip `#{keyword}`")

        if await db.is_snip(client.me.id, message.chat.id, keyword.lower()):
            data = await db.get_snip(client.me.id, message.chat.id, keyword.lower())
            data = data["snips"][0]
            file_id = data.get("fileId", None)
            caption = data.get("text", None)

            if file_id:
                sent = await message.reply_cached_media(file_id, caption=caption)
                await sent.reply_text(f"**🍀 𝖲𝗇𝗂𝗉 𝖭𝗈𝗍𝖾:** `#{keyword}`")
                await hell.delete()
            else:
                await hell.edit(f"**🍀 𝖲𝗇𝗂𝗉 𝖭𝗈𝗍𝖾:** `#{keyword}`\n\n{caption}")

        else:
            await hellbot.delete(hell, f"**🍀 𝖲𝗇𝗂𝗉 𝖭𝗈𝗍𝖾 𝖽𝗈𝖾𝗌 𝗇𝗈𝗍 𝖾𝗑𝗂𝗌𝗍𝗌:** `#{keyword}`")

    else:
        hell = await hellbot.edit(message, "Getting all snips...")
        snips = await db.get_all_snips(client.me.id, message.chat.id)
        if snips:
            text = f"**🍀 𝖭𝗈. 𝗈𝖿 𝖲𝗇𝗂𝗉 𝖭𝗈𝗍𝖾 𝗂𝗇 𝗍𝗁𝗂𝗌 𝖼𝗁𝖺𝗍:** `{len(snips)}`\n\n"

            for i, snip in enumerate(snips, 1):
                text += f"** {'0' if i < 10 else ''}{i}:** `#{snip['keyword']}`\n"

            await hell.edit(text)

        else:
            await hellbot.delete(hell, "No snip note saved in this chat.")


@custom_handler(filters.incoming & filters.regex(r"^#\s*(.*)$") & filters.text)
async def snipHandler(client: Client, message: Message):
    keyword = message.text.split("#", 1)[1].lower()
    if await db.is_snip(client.me.id, message.chat.id, keyword):
        data = await db.get_snip(client.me.id, message.chat.id, keyword)
        data = data["snips"][0]
        file_id = data.get("fileId", None)
        caption = data.get("text", None)

        reply_to = message.reply_to_message.id if message.reply_to_message else None
        if file_id:
            await client.send_cached_media(
                message.chat.id,
                file_id,
                caption,
                reply_to_message_id=reply_to,
            )
        else:
            await client.send_message(
                message.chat.id,
                caption,
                disable_web_page_preview=True,
                reply_to_message_id=reply_to,
            )


HelpMenu("snips").add(
    "snip",
    "<keyword> <reply to message>",
    "Save the replied message as a snip note.",
    "snip hello",
    "An alias of 'note' is also available.",
).add(
    "rmsnip", "<keyword>", "Remove the snip note.", "rmsnip hello"
).add(
    "rmallsnip", None, "Remove all snip notes.", "rmallsnip"
).add(
    "getsnip",
    "<keyword>",
    "Get the snip note.",
    "getsnip hello",
).add(
    "snips",
    None,
    "Get all snip notes.",
    "snips",
).info(
    "Snips are triggered when # is used before the keyword."
).done()
