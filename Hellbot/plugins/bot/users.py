from pyrogram import Client, filters
from pyrogram.types import Message

from . import BotHelp, Config, Symbols, hellbot


@hellbot.bot.on_message(
    filters.command("addauth") & Config.AUTH_USERS & filters.private
)
async def addauth(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "Give me a userid/username to add them as an auth user!"
        )

    try:
        user = await client.get_users(message.command[1])
    except Exception:
        return await message.reply_text(
            "Give me a valid userid/username to add them as an auth user!"
        )

    if user.is_self:
        return await message.reply_text("I can't add myself as an auth user!")

    if user.id in Config.AUTH_USERS:
        return await message.reply_text(f"**{user.mention} is already authorized**")

    Config.AUTH_USERS.add(user.id)
    await message.reply_text(f"**Added {user.mention} to auth users!**")


@hellbot.bot.on_message(
    filters.command("delauth") & Config.AUTH_USERS & filters.private
)
async def delauth(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "Give me a userid/username to remove them from auth users!"
        )

    try:
        user = await client.get_users(message.command[1])
    except Exception:
        return await message.reply_text(
            "Give me a valid userid/username to remove them from auth users!"
        )

    if user.id in Config.AUTH_USERS:
        Config.AUTH_USERS.remove(user.id)
        await message.reply_text(f"**Removed {user.mention} from auth users!**")
    else:
        await message.reply_text(f"**{user.mention} is not authorized**")


@hellbot.bot.on_message(
    filters.command("authlist") & Config.AUTH_USERS & filters.private
)
async def authlist(client: Client, message: Message):
    text = "**🍀 Authorized Users:**\n\n"
    for userid in Config.AUTH_USERS:
        user = await client.get_users(userid)
        text += f"    {Symbols.anchor} {user.mention} (`{user.id}`)\n"

    await message.reply_text(text)


BotHelp("users").add(
    "addauth",
    "This command is used to add a user as an authorized user. An authorized user can create and manage userbot session!",
).add("delauth", "This command is used to remove a user from authorized users.").add(
    "authlist", "This command is used to list all authorized users."
).info(
    "Users Command 🚀"
).done()
