import re

from pyrogram import Client
from pyrogram.types import Message

from . import HelpMenu, Symbols, handler, hellbot, on_message


@on_message("newfed", allow_stan=True)
async def newfed(client: Client, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(message, f"Usage: {handler}newfed <fedname>")

    bot_un = "@MissRose_bot"
    await client.unblock_user(bot_un)

    fedname = await hellbot.input(message)
    hell = await hellbot.edit(message, f"__Creating new federation__ **{fedname}**")

    extract_fedid = (
        lambda text: re.search(r"FedID: (\S+)", text).group(1)
        if re.search(r"FedID: (\S+)", text)
        else None
    )

    try:
        msg1 = await client.ask(bot_un, f"/newfed {fedname}", timeout=60)
    except Exception as e:
        return await hellbot.error(hell, f"`{e}`")

    if "created new federation" in msg1.text.lower():
        await hell.edit(
            f"**𝖭𝖾𝗐 𝖥𝖾𝖽𝖾𝗋𝖺𝗍𝗂𝗈𝗇 𝖼𝗋𝖾𝖺𝗍𝖾𝖽 𝗈𝗇 {bot_un}:** `{fedname}` \n**𝖥𝖾𝖽𝖨𝖽:** `{extract_fedid(msg1.text)[:-1]}`"
        )
    else:
        await hellbot.delete(hell, f"**Failed to create federation!**\n\n`{msg1.text}`")

    try:
        await msg1.request.delete()
        await msg1.delete()
    except:
        pass


@on_message("renamefed", allow_stan=True)
async def renamefed(client: Client, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(message, f"Usage: {handler}renamefed <new fedname>")

    bot_un = "@MissRose_bot"
    await client.unblock_user(bot_un)

    fedname = await hellbot.input(message)
    hell = await hellbot.edit(message, f"__Renaming federation to__ **{fedname}**")

    try:
        msg1 = await client.ask(bot_un, f"/renamefed {fedname}", timeout=60)
    except Exception as e:
        return await hellbot.error(hell, f"`{e}`")

    if "renamed your federation from" in msg1.text.lower():
        await hell.edit(f"**𝖥𝖾𝖽𝖾𝗋𝖺𝗍𝗂𝗈𝗇 𝗋𝖾𝗇𝖺𝗆𝖾𝖽 𝗍𝗈** `{fedname}`")
    else:
        await hellbot.delete(hell, f"**Failed to rename federation!**\n\n`{msg1.text}`")

    try:
        await msg1.request.delete()
        await msg1.delete()
    except:
        pass


@on_message("fedinfo", allow_stan=True)
async def fedinfo(client: Client, message: Message):
    if len(message.command) < 2:
        fedid = ""
    else:
        fedid = message.command[1]

    bot_un = "@MissRose_bot"
    await client.unblock_user(bot_un)

    get_value = lambda pattern: pattern.group(1) if pattern else None
    hell = await hellbot.edit(message, "__Fetching federation info__")

    try:
        msg1 = await client.ask(bot_un, f"/fedinfo {fedid}", timeout=60)
    except Exception as e:
        return await hellbot.error(hell, f"`{e}`")

    if "fed info" in msg1.text.lower():
        fedid, name, creator, admins, bans, connected_chats, subscribed_feds = map(
            get_value,
            (
                re.search(r"FedID: (\S+)", msg1.text),
                re.search(r"Name: (.+)", msg1.text),
                re.search(r"Creator: (.+)", msg1.text),
                re.search(r"admins: (\d+)", msg1.text),
                re.search(r"bans: (\d+)", msg1.text),
                re.search(r"connected chats: (\d+)", msg1.text),
                re.search(r"subscribed feds: (\d+)", msg1.text),
            ),
        )

        await hell.edit(
            f"**{Symbols.anchor} 𝖥𝖾𝖽𝖨𝖽:** `{fedid}`\n"
            f"**{Symbols.anchor} 𝖭𝖺𝗆𝖾:** `{name}`\n"
            f"**{Symbols.anchor} 𝖢𝗋𝖾𝖺𝗍𝗈𝗋:** {creator}\n"
            f"**{Symbols.anchor} 𝖳𝗈𝗍𝖺𝗅 𝖺𝖽𝗆𝗂𝗇𝗌:** `{admins}`\n"
            f"**{Symbols.anchor} 𝖳𝗈𝗍𝖺𝗅 𝖻𝖺𝗇𝗌::** `{bans}`\n"
            f"**{Symbols.anchor} 𝖢𝗈𝗇𝗇𝖾𝖼𝗍𝖾𝖽 𝖢𝗁𝖺𝗍𝗌:** `{connected_chats}`\n"
            f"**{Symbols.anchor} 𝖲𝗎𝖻𝗌𝖼𝗋𝗂𝖻𝖾𝖽 𝖥𝖾𝖽𝖲:** `{subscribed_feds}`\n"
        )
    else:
        await hellbot.delete(hell, f"**Failed to fetch federation info!**\n\n`{msg1.text}`")

    try:
        await msg1.request.delete()
        await msg1.delete()
    except:
        pass


HelpMenu("federation").add(
    "newfed", "<name>", "Create a new federation on Rose Bot.", "newfed Example Name",  
).add(
    "renamefed", "<name>", "Rename your federation on Rose Bot.", "renamefed Example Name",
).add(
    "fedinfo", "<fedid>", "Get info about a federation on Rose Bot.", "fedinfo fed-id",
).info(
    "MissRose Federation"
).done()
