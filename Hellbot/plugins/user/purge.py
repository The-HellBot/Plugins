import asyncio

from pyrogram import Client
from pyrogram.types import Message

from . import HelpMenu, hellbot, on_message


def _chunk(from_msg: int, to_msg: int):
    curr_msg = from_msg

    while curr_msg < to_msg:
        yield list(range(curr_msg, min(curr_msg + 100, to_msg)))
        curr_msg += 100


@on_message("purge", allow_stan=True)
async def purgeMsg(client: Client, message: Message):
    if not message.reply_to_message:
        return await hellbot.delete(
            message, "__Reply to a message to delete all messages after that.__"
        )

    deleted = 0
    from_msg = message.reply_to_message

    hell = await hellbot.edit(message, "__Purging...__")
    for msg_ids in _chunk(from_msg.id, message.id + 1):
        try:
            status = await client.delete_messages(message.chat.id, msg_ids)
            deleted += status
        except:
            pass

    await hellbot.delete(hell, f"__🧹 Purged {deleted} messages.__")


@on_message("purgeme", allow_stan=True)
async def purgeMe(client: Client, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(
            message, "__Give the number of messages you want to delete.__"
        )
    try:
        count = int(message.command[1])
    except:
        return await hellbot.delete(message, "Argument must be an integer.")

    hell = await hellbot.edit(message, "__Purging...__")
    async for msgs in client.search_messages(
        message.chat.id, limit=count, from_user="me"
    ):
        try:
            await msgs.delete()
        except:
            pass

    await hellbot.delete(hell, f"__🧹 Purged {count} messages.__")


@on_message("purgeuser", allow_stan=True)
async def purgeUser(client: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.from_user:
        return await hellbot.delete(
            message, "__Reply to a user to delete their messages.__"
        )

    count = 0
    if len(message.command) > 1:
        try:
            count = int(message.command[1])
        except:
            return await hellbot.delete(message, "Argument must be an integer.")

    hell = await hellbot.edit(message, "__Purging...__")
    async for msgs in client.search_messages(
        message.chat.id, limit=count, from_user=message.reply_to_message.from_user.id
    ):
        try:
            await msgs.delete()
        except:
            pass

    await hellbot.delete(
        hell,
        f"__🧹 Purged {count} messages of {message.reply_to_message.from_user.mention}.__,,"
    )


@on_message("del", allow_stan=True)
async def delMsg(_, message: Message):
    if not message.reply_to_message:
        return await hellbot.delete(
            message, "__Reply to a message to delete that message.__"
        )

    await message.reply_to_message.delete()
    await message.delete()


@on_message(["selfdestruct", "sd"], allow_stan=True)
async def selfdestruct(client: Client, message: Message):
    if len(message.command) < 3:
        return await hellbot.delete(
            message, "__Give the number of seconds and the message to self-destruct.__"
        )

    try:
        seconds = int(message.command[1])
    except:
        return await hellbot.delete(message, "Argument must be an integer.")

    msg = " ".join(message.command[2:])
    await message.delete()
    x = await client.send_message(message.chat.id, msg)
    await asyncio.sleep(seconds)
    await x.delete()


HelpMenu("purge").add(
    "purge",
    "<reply to message>",
    "Deletes all messages after the replied message.",
    "purge",
).add(
    "purgeme",
    "<count>",
    "Deletes last x number of your messages.",
    "purgeme 69",
).add(
    "purgeuser",
    "<reply to user> <count>",
    "Deletes last x number of messages of replied user.",
    "purgeuser @ForGo10God 69",
).add(
    "del",
    "<reply to message>",
    "Deletes the replied message.",
    "del",
).add(
    "selfdestruct",
    "<seconds> <message>",
    "Sends a message and deletes it after x seconds.",
    "selfdestruct 10 Hello World!",
    "An alias of 'sd' is also available.",
).info(
    "Bulk delete messages."
).done()
