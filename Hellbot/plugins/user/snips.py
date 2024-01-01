from pyrogram import Client, filters
from pyrogram.types import Message

from . import Config, HelpMenu, custom_handler, db, handler, hellbot, on_message


@on_message(["snip", "note"], allow_stan=True)
async def addsnip(client: Client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await hellbot.delete(
            message,
            f"Reply to a message with {handler}snip <keyword> to save it as a snip.",
        )

    keyword = (await hellbot.input(message)).replace("#", "")
    hell = await hellbot.edit(message, f"Saving snip `#{keyword}`")
    msg = await message.reply_to_message.forward(Config.LOGGER_ID)

    await db.set_snip(client.me.id, message.chat.id, keyword.lower(), msg.id)
    await hellbot.delete(hell, f"**📌 𝖭𝖾𝗐 𝖲𝗇𝗂𝗉 𝖭𝗈𝗍𝖾 𝖲𝖺𝗏𝖾𝖽:** `#{keyword}`")
    await msg.reply_text(
        f"**📌 𝖭𝖾𝗐 𝖲𝗇𝗂𝗉 𝖭𝗈𝗍𝖾 𝖲𝖺𝗏𝖾𝖽:** `#{keyword}`\n\n**DO NOT DELETE THIS MESSAGE!!!**",
    )


@on_message(["rmsnip", "rmallsnip"], allow_stan=True)
async def rmsnip(client: Client, message: Message):
    if len(message.command[0]) < 7:
        if len(message.command) < 2:
            return await hellbot.delete(message, "Give a snip note name to remove.")

        keyword = (await hellbot.input(message)).replace("#", "")
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
            msgid = data["snips"][0]["msgid"]
            sent = await client.copy_message(message.chat.id, Config.LOGGER_ID, msgid)

            await sent.reply_text(f"**🍀 𝖲𝗇𝗂𝗉 𝖭𝗈𝗍𝖾:** `#{keyword}`")
            await hell.delete()
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


@custom_handler(
    filters.incoming & filters.regex(r"^#\s*(.*)$") & filters.text & ~filters.service
)
async def snipHandler(client: Client, message: Message):
    keyword = message.text.split("#", 1)[1].lower()
    if await db.is_snip(client.me.id, message.chat.id, keyword):
        data = await db.get_snip(client.me.id, message.chat.id, keyword)
        msgid = data["snips"][0]["msgid"]

        reply_to = (
            message.reply_to_message.id if message.reply_to_message else message.id
        )
        await client.copy_message(
            message.chat.id, Config.LOGGER_ID, msgid, reply_to_message_id=reply_to
        )


HelpMenu("snips").add(
    "snip",
    "<keyword> <reply to message>",
    "Save the replied message as a snip note.",
    "snip hello",
    "An alias of 'note' is also available.",
).add("rmsnip", "<keyword>", "Remove the snip note.", "rmsnip hello").add(
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
