from pyrogram import Client, filters
from pyrogram.types import Message

from Hellbot.core import Symbols

from . import HelpMenu, custom_handler, db, group_n_channel, hellbot, on_message


@on_message("autopost", chat_type=group_n_channel, allow_stan=True)
async def autopost(client: Client, message: Message):
    if len(message.command) != 2:
        return await hellbot.delete(
            message, "Wrong usage of command.\nCheck help menu for more info."
        )

    hell = await hellbot.edit(message, "Starting Autopost in this group/channel...")

    post_from = message.command[1]
    _chat = await client.get_chat(post_from)

    if not _chat:
        return await hellbot.delete(hell, "Invalid chat/channel id.")

    if _chat.type not in group_n_channel:
        return await hellbot.delete(
            hell, "You can only autopost in groups and channels."
        )

    if _chat.id == message.chat.id:
        return await hellbot.delete(
            hell, "You can't autopost in the same group/channel."
        )

    if _chat.id in await db.is_autopost(client.me.id, _chat.id, message.chat.id):
        return await hellbot.delete(
            hell, "This group/channel is already in autopost list."
        )

    await db.set_autopost(client.me.id, _chat.id, message.chat.id)

    await hellbot.delete(
        hell, f"Autopost started from {_chat.title} to {message.chat.title}."
    )
    await hellbot.check_and_log(
        "autopost start",
        f"**AutoPost From:** {_chat.title} \n**AutoPost To:** {message.chat.title}\n**AutoPost By:** {client.me.mention}",
    )


@on_message("stopautopost", chat_type=group_n_channel, allow_stan=True)
async def stop_autopost(client: Client, message: Message):
    if len(message.command) != 2:
        return await hellbot.delete(
            message, "Wrong usage of command.\nCheck help menu for more info."
        )

    hell = await hellbot.edit(message, "Stopping Autopost in this group/channel...")

    post_from = message.command[1]
    _chat = await client.get_chat(post_from)

    if not _chat:
        return await hellbot.delete(hell, "Invalid chat/channel id.")

    if _chat.type not in group_n_channel:
        return await hellbot.delete(
            hell, "You can only autopost in groups and channels."
        )

    if _chat.id not in await db.is_autopost(client.me.id, _chat.id, message.chat.id):
        return await hellbot.delete(hell, "This group/channel is not in autopost list.")

    await db.rm_autopost(client.me.id, _chat.id, message.chat.id)

    await hellbot.delete(
        hell, f"Autopost stopped from {_chat.title} to {message.chat.title}."
    )
    await hellbot.check_and_log(
        "autopost stop",
        f"**AutoPost From:** {_chat.title} \n**AutoPost To:** {message.chat.title}\n**AutoPost By:** {client.me.mention}",
    )


@on_message("autoposts", chat_type=group_n_channel, allow_stan=True)
async def autoposts(client: Client, message: Message):
    hell = await hellbot.edit(message, "Getting autopost list...")

    data = await db.get_all_autoposts(client.me.id)
    if not data:
        return await hellbot.delete(hell, "No autoposts found.")

    text = f"**𝖠𝖼𝗍𝗂𝗏𝖾 𝖠𝗎𝗍𝗈𝗉𝗈𝗌𝗍𝗌 𝖿𝗈𝗋: {client.me.mention}**\n\n"
    for i in data:
        from_chat = await client.get_chat(i["from_channel"])
        to_chat = await client.get_chat(i["to_channel"])

        from_chat_name = (
            f"{from_chat.title} [{from_chat.id}]" if from_chat else i["from_channel"]
        )
        to_chat_name = f"{to_chat.title} [{to_chat.id}]" if to_chat else i["to_channel"]

        text += f"   {Symbols.anchor} **From:** {from_chat_name}\n"
        text += f"   {Symbols.anchor} **To:** {to_chat_name}\n"
        text += f"   {Symbols.anchor} **Date:** {i['date']}\n\n"

    await hellbot.edit(hell, text)


@custom_handler(filters.incoming & filters.group & filters.channel & ~filters.service)
async def handle_autopost(client: Client, message: Message):
    if not await db.is_autopost(client.me.id, message.chat.id):
        return

    data = await db.get_autopost(client.me.id, message.chat.id)
    if not data:
        return

    from_chat = await client.get_chat(data["from_channel"])
    if not from_chat:
        return

    if message.chat.id != data["to_channel"]:
        return

    await message.copy(int(data["to_channel"]))


HelpMenu("autopost").add(
    "autopost",
    "<channel id>",
    "Start autoposting in current group/channel from the mentioned chatid/username of channel.",
    "autopost @Its_HellBot",
    "This module will post all incoming post from the target channel to the current chat without forward tag!",
).add(
    "stopautopost",
    "<channel id>",
    "Stops autoposting in current chroup/channel from the mentioned chatid/username of channel.",
    "stopautopost @Its_HellBot",
).add(
    "autoposts", None, "Get all active autoposts!", "autoposts"
).info(
    "AutoPost Module"
).done()
