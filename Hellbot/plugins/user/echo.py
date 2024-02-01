import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from Hellbot.core import Symbols

from . import HelpMenu, custom_handler, db, hellbot, on_message


@on_message("echo", allow_stan=True)
async def echo(client: Client, message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        user = (await client.get_users(message.command[1])).id
    else:
        return await hellbot.delete(
            message, "Reply to an user or pass me a user id to start echoing!"
        )

    if await db.is_echo(client.me.id, message.chat.id, user):
        return await hellbot.delete(message, "Echo is already enabled for this user!")

    await db.set_echo(client.me.id, message.chat.id, user)
    await hellbot.delete(message, "Echo enabled for this user!")


@on_message("unecho", allow_stan=True)
async def unecho(client: Client, message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        user = (await client.get_users(message.command[1])).id
    else:
        return await hellbot.delete(
            message, "Reply to an user or pass me a user id to stop echoing!"
        )

    if not await db.is_echo(client.me.id, message.chat.id, user):
        return await hellbot.delete(message, "Echo is already disabled for this user!")

    await db.rm_echo(client.me.id, message.chat.id, user)
    await hellbot.delete(message, "Echo disabled for this user!")


@on_message("listecho", allow_stan=True)
async def listecho(client: Client, message: Message):
    echos = await db.get_all_echo(client.me.id, message.chat.id)
    if not echos:
        return await hellbot.delete(message, "No echos in this chat!")

    text = "**𝖫𝗂𝗌𝗍 𝗈𝖿 𝖤𝖼𝗁𝗈 𝗂𝗇 𝗍𝗁𝗂𝗌 𝖼𝗁𝖺𝗍:**\n\n"
    for echo in echos:
        text += f"    {Symbols.anchor} `{echo}`\n"

    await hellbot.edit(message, text)


@custom_handler(filters.incoming & filters.text & filters.sticker & ~filters.service)
async def echo_handler(client: Client, message: Message):
    if not await db.is_echo(client.me.id, message.chat.id, message.from_user.id):
        return

    if message.sticker:
        await message.reply_sticker(message.sticker.file_id)
    else:
        await message.reply(message.text)


@on_message(["resend", "copy"], allow_stan=True)
async def reSend(_, message: Message):
    if message.reply_to_message:
        await message.reply_to_message.copy(
            message.chat.id, reply_to_message_id=message.reply_to_message.id
        )
    await message.delete()


HelpMenu("echo").add(
    "echo",
    "<reply> or <userid>",
    "Echo every message of the replied user in present chat!",
    "echo @ForGo10God",
    "Echo works on text and sticker messages only!",
).add(
    "unecho",
    "<reply> or <userid>",
    "Stop echoing messages of the replied user in present chat!",
    "unecho @ForGo10God",
).add(
    "listecho",
    None,
    "List all the users whose messages are being echoed in present chat!",
    "listecho",
).add(
    "resend",
    "<reply>",
    "Resend the replied message!",
    "resend",
    "An alias of 'copy' is also available!",
).info(
    "Is it Echoing?"
).done()
