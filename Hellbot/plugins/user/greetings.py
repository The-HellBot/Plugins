from pyrogram import Client, filters
from pyrogram.types import Message

from . import Config, HelpMenu, custom_handler, db, hellbot, on_message

GREETINGS_CACHE = {
    "welcome": {},
    "goodbye": {},
}


GREETINGS_FORMATTINGS = """
`{first}` - __First name of the user who joined/left.__
`{last}` - __Last name of the user who joined/left.__
`{fullname}` - __Full name of the user who joined/left.__
`{mention}` - __Mentions the user who joined/left.__
`{username}` - __Username of the user who joined/left.__
`{userid}` - __ID of the user who joined/left.__
`{chatname}` - __Name of the chat.__
`{chatid}` - __ID of the chat.__

**📌 Note:**
  ▸ These formattings are only available for welcome and goodbye messages.
  ▸ These are case sensitive. Use them as they are.
  ▸ Every formatting are optional. You can use any of them or none of them.
"""


@on_message("greetings", allow_stan=True)
async def greetingsformat(_, message: Message):
    await hellbot.edit(message, GREETINGS_FORMATTINGS)


@on_message("welcome", allow_stan=True)
async def getwelcome(client: Client, message: Message):
    welcome = await db.get_welcome(client.me.id, message.chat.id)

    if not welcome:
        return await hellbot.edit(message, "No welcome message in this chat.")

    msg = await client.get_messages(Config.LOGGER_ID, welcome["message"])

    await msg.copy(message.chat.id, reply_to_message_id=message.id)
    await hellbot.edit(message, "Welcome message sent.")


@on_message("setwelcome", allow_stan=True)
async def setwelcome(client: Client, message: Message):
    if not message.reply_to_message:
        return await hellbot.edit(
            message, "Reply to a message to set it as welcome message."
        )

    msg = await message.reply_to_message.forward(Config.LOGGER_ID)
    await db.set_welcome(client.me.id, message.chat.id, msg.id)

    await hellbot.delete(message, f"**Welcome message saved for** {message.chat.title}")
    await msg.reply_text(
        f"Welcome message set for {message.chat.title}({message.chat.id})\n\n**DO NOT DELETE THE REPLIED MESSAGE!!!**"
    )


@on_message("delwelcome", allow_stan=True)
async def delwelcome(client: Client, message: Message):
    if await db.is_welcome(client.me.id, message.chat.id):
        await db.rm_welcome(client.me.id, message.chat.id)
        await hellbot.delete(message, "Welcome message deleted.")
    else:
        await hellbot.delete(message, "No welcome message in this chat.")


@on_message("goodbye", allow_stan=True)
async def getgoodbye(client: Client, message: Message):
    goodbye = await db.get_goodbye(client.me.id, message.chat.id)

    if not goodbye:
        return await hellbot.edit(message, "No goodbye message in this chat.")

    msg = await client.get_messages(Config.LOGGER_ID, goodbye["message"])

    await msg.copy(message.chat.id, reply_to_message_id=message.id)
    await hellbot.edit(message, "Goodbye message sent.")


@on_message("setgoodbye", allow_stan=True)
async def setgoodbye(client: Client, message: Message):
    if not message.reply_to_message:
        return await hellbot.edit(
            message, "Reply to a message to set it as goodbye message."
        )

    msg = await message.reply_to_message.forward(Config.LOGGER_ID)
    await db.set_goodbye(client.me.id, message.chat.id, msg.id)

    await hellbot.delete(message, f"**Goodbye message saved for** {message.chat.title}")
    await msg.reply_text(
        f"Goodbye message set for {message.chat.title}({message.chat.id})\n\n**DO NOT DELETE THE REPLIED MESSAGE!!!**"
    )


@on_message("delgoodbye", allow_stan=True)
async def delgoodbye(client: Client, message: Message):
    if await db.is_goodbye(client.me.id, message.chat.id):
        await db.rm_goodbye(client.me.id, message.chat.id)
        await hellbot.delete(message, "Goodbye message deleted.")
    else:
        await hellbot.delete(message, "No goodbye message in this chat.")


@custom_handler(filters.new_chat_members & filters.group)
async def welcomehandler(client: Client, message: Message):
    if not message.from_user:
        return

    welcome = await db.get_welcome(client.me.id, message.chat.id)
    if not welcome:
        return

    msg = await client.get_messages(Config.LOGGER_ID, welcome["message"])
    if message.media:
        text = message.caption if message.caption else None
    else:
        text = message.text if message.text else None

    if text:
        first = message.new_chat_members[0].first_name
        last = (
            message.new_chat_members[0].last_name
            if message.new_chat_members[0].last_name
            else ""
        )
        mention = message.new_chat_members[0].mention
        username = message.new_chat_members[0].username
        text = text.format(
            first=first,
            last=last,
            fullname=f"{first} {last}",
            mention=mention,
            username=f"@{username}" if username else mention,
            userid=message.new_chat_members[0].id,
            chatname=message.chat.title,
            chatid=message.chat.id,
        )

    to_del = await msg.copy(
        message.chat.id,
        text,
        reply_to_message_id=message.id,
    )

    if message.chat.id in GREETINGS_CACHE["welcome"]:
        msg: Message = GREETINGS_CACHE.get("welcome", {}).get(message.chat.id)
        await msg.delete()
        GREETINGS_CACHE["welcome"][message.chat.id] = to_del
    else:
        GREETINGS_CACHE["welcome"][message.chat.id] = to_del


@custom_handler(filters.left_chat_member & filters.group)
async def goodbyehandler(client: Client, message: Message):
    if not message.from_user:
        return

    goodbye = await db.get_goodbye(client.me.id, message.chat.id)
    if not goodbye:
        return

    msg = await client.get_messages(Config.LOGGER_ID, goodbye["message"])
    if message.media:
        text = message.caption if message.caption else None
    else:
        text = message.text if message.text else None

    if text:
        first = message.new_chat_members[0].first_name
        last = (
            message.new_chat_members[0].last_name
            if message.new_chat_members[0].last_name
            else ""
        )
        mention = message.new_chat_members[0].mention
        username = message.new_chat_members[0].username
        text = text.format(
            first=first,
            last=last,
            fullname=f"{first} {last}",
            mention=mention,
            username=f"@{username}" if username else mention,
            userid=message.new_chat_members[0].id,
            chatname=message.chat.title,
            chatid=message.chat.id,
        )

    to_del = await msg.copy(
        message.chat.id,
        text,
        reply_to_message_id=message.id,
    )

    if message.chat.id in GREETINGS_CACHE["goodbye"]:
        msg: Message = GREETINGS_CACHE.get("goodbye", {}).get(message.chat.id)
        await msg.delete()
        GREETINGS_CACHE["goodbye"][message.chat.id] = to_del
    else:
        GREETINGS_CACHE["goodbye"][message.chat.id] = to_del


HelpMenu("greetings").add(
    "greetings",
    None,
    "Get the formattings for welcome and goodbye messages.",
).add(
    "welcome",
    None,
    "Get saved welcome message for current chat.",
    "welcome",
    "A welcome message will be sent to the chat when a new user joins.",
).add(
    "setwelcome",
    "<reply to a message>",
    "Set the replied message as welcome message for current chat.",
    "setwelcome",
    "A welcome message will be sent to the chat when a new user joins.",
).add(
    "delwelcome",
    None,
    "Delete the welcome message for current chat.",
    "delwelcome",
).add(
    "goodbye",
    None,
    "Get saved goodbye message for current chat.",
    "goodbye",
    "A goodbye message will be sent to the chat when a user leaves.",
).add(
    "setgoodbye",
    None,
    "Set the replied message as goodbye message for current chat.",
    "setgoodbye",
    "A goodbye message will be sent to the chat when a user leaves.",
).add(
    "delgoodbye",
    None,
    "Delete the goodbye message for current chat.",
    "delgoodbye",
    "A goodbye message will be sent to the chat when a user leaves.",
).info(
    "Welcome and Goodbye Messages"
).done()
