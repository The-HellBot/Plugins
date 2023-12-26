import asyncio

from pyrogram import Client
from pyrogram.types import Message

from . import HelpMenu, Symbols, hellbot, on_message

spamTask = {}


async def spam_text(
    client: Client,
    chat_id: int,
    to_spam: str,
    count: int,
    reply_to: int,
    delay: float,
    copy_id: int,
    event: asyncio.Event,
):
    for _ in range(count):
        if event.is_set():
            break

        if copy_id:
            await client.copy_message(
                chat_id, chat_id, copy_id, reply_to_message_id=reply_to
            )
        else:
            await client.send_message(
                chat_id,
                to_spam,
                disable_web_page_preview=True,
                reply_to_message_id=reply_to,
            )
        if delay:
            await asyncio.sleep(delay)

    try:
        event.set()
        task = spamTask.get(chat_id, None)
        if task:
            task.remove(event)
    except:
        pass

    await hellbot.check_and_log(
        "spam",
        f"**Count:** `{count}`\n**Chat:** `{chat_id}`\n**Client:** {client.me.first_name}",
    )


@on_message("spam", allow_stan=True)
async def spamMessage(client: Client, message: Message):
    if len(message.command) < 3:
        return await hellbot.delete(message, "Give me something to spam.")

    reply_to = message.reply_to_message.id if message.reply_to_message else None
    try:
        count = int(message.command[1])
    except ValueError:
        return await hellbot.delete(message, "Give me a valid number to spam.")

    to_spam = message.text.split(" ", 2)[2].strip()
    event = asyncio.Event()
    task = asyncio.create_task(
        spam_text(client, message.chat.id, to_spam, count, reply_to, None, None, event)
    )

    if spamTask.get(message.chat.id, None):
        spamTask[message.chat.id].append(event)
    else:
        spamTask[message.chat.id] = [event]

    await message.delete()
    await task


@on_message("dspam", allow_stan=True)
async def delaySpam(client: Client, message: Message):
    if len(message.command) < 4:
        return await hellbot.delete(message, "Give me something to spam.")

    reply_to = message.reply_to_message.id if message.reply_to_message else None
    try:
        count = int(message.command[1])
    except ValueError:
        return await hellbot.delete(message, "Give me a valid number to spam.")

    try:
        delay = float(message.command[2])
    except ValueError:
        return await hellbot.delete(message, "Give me a valid delay to spam.")

    to_spam = message.text.split(" ", 3)[3].strip()
    event = asyncio.Event()
    task = asyncio.create_task(
        spam_text(client, message.chat.id, to_spam, count, reply_to, delay, None, event)
    )

    if spamTask.get(message.chat.id, None):
        spamTask[message.chat.id].append(event)
    else:
        spamTask[message.chat.id] = [event]

    await message.delete()
    await task


@on_message("mspam", allow_stan=True)
async def mediaSpam(client: Client, message: Message):
    if not message.reply_to_message:
        return await hellbot.delete(message, "Reply to a media to spam.")

    if len(message.command) < 2:
        return await hellbot.delete(message, "Give me a valid number to spam.")

    try:
        count = int(message.command[1])
    except ValueError:
        return await hellbot.delete(message, "Give me a valid number to spam.")

    copy_id = message.reply_to_message.id
    event = asyncio.Event()
    task = asyncio.create_task(
        spam_text(client, message.chat.id, None, count, None, None, copy_id, event)
    )

    if spamTask.get(message.chat.id, None):
        spamTask[message.chat.id].append(event)
    else:
        spamTask[message.chat.id] = [event]

    await message.delete()
    await task


@on_message("stopspam", allow_stan=True)
async def stopSpam(_, message: Message):
    chat_id = message.chat.id

    if not spamTask.get(chat_id, None):
        return await hellbot.delete(message, "No spam task running for this chat.")

    for event in spamTask[chat_id]:
        event.set()

    chat_name = message.chat.title or message.chat.first_name
    del spamTask[chat_id]
    await hellbot.delete(message, f"Spam task stopped for {chat_name}.")


@on_message("listspam", allow_stan=True)
async def listSpam(_, message: Message):
    active_spams = list(spamTask.keys())

    text = "**Active Spam Tasks:**\n\n"
    for active in active_spams:
        text += f"{Symbols.anchor} `{active}`\n"

    await hellbot.edit(message, text)


HelpMenu("spam").add(
    "spam",
    "<count> <message>",
    "Spam a message in the chat for x times.",
    "spam 10 hi",
    "Spamming may get you banned.",
).add(
    "dspam",
    "<count> <delay> <message>",
    "Spam a message in the chat for x times with delay. Delay must be in seconds.",
    "dspam 10 1 hi",
    "Spamming may get you banned.",
).add(
    "mspam",
    "<count> <reply to media>",
    "Spam a media in the chat for x times.",
    "mspam 10",
    "Spamming may get you banned.",
).add(
    "stopspam",
    None,
    "Stop all spam tasks running in the chat.",
    "stopspam",
    "This command is chat dependent.",
).add(
    "listspam",
    None,
    "List all active spam tasks in the bot.",
    "listspam",
).info(
    "Spam Messages"
).done()
