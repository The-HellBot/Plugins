from pyrogram import Client
from pyrogram.types import Message

from . import Config, HelpMenu, db, hellbot, on_message


@on_message("stan", allow_stan=True)
async def stanUsers(client: Client, message: Message):
    hell = await hellbot.edit(message, "__Fetching users...__")

    users = await db.get_stans(client.me.id)
    if not users:
        return await hellbot.delete(hell, "__No stans found!__")

    text = f"**Total stans:** `{len(users)}`\n\n"
    for user in users:
        try:
            user = await client.get_users(user["user_id"])
            mention = user.mention
            userid = user.id
        except Exception:
            userid = user["user_id"]
            mention = "Unknown Peer"
        text += f"• {mention} (`{userid}`)\n"

    await hell.edit(text)


@on_message("addstan", allow_stan=False)
async def addstan(client: Client, message: Message):
    if len(message.command) < 2:
        if not message.reply_to_message:
            return await hellbot.delete(
                message,
                "__Reply to a user or give me a user id to add them as a stan!__",
            )
        user = message.reply_to_message.from_user
    else:
        try:
            user = await client.get_users(message.command[1])
        except Exception:
            return await hellbot.delete(
                message, "__Give me a valid user id to add them as a stan!__"
            )

    if user.id == client.me.id:
        return await hellbot.delete(message, "__I can't be a stan of myself!__")

    if await db.is_stan(client.me.id, user.id):
        return await hellbot.delete(message, "__This user is already a stan!__")

    await db.add_stan(client.me.id, user.id)
    await hellbot.delete(message, f"__Added {user.mention} as a stan!__")

    Config.AUTH_USERS.add(user.id)
    Config.STAN_USERS.add(user.id)


@on_message("delstan", allow_stan=False)
async def delstan(client: Client, message: Message):
    if len(message.command) < 2:
        if not message.reply_to_message:
            return await hellbot.delete(
                message,
                "__Reply to a user or give me a user id to remove them from stans!__",
            )
        user = message.from_user
    else:
        try:
            user = await client.get_users(message.command[1])
        except Exception:
            return await hellbot.delete(
                message, "__Give me a valid user id to remove them from stans!__"
            )

    if await db.is_stan(client.me.id, user.id):
        await db.rm_stan(client.me.id, user.id)
        await hellbot.delete(message, f"__Removed {user.mention} from stans!__")

        Config.AUTH_USERS.remove(user.id)
        Config.STAN_USERS.remove(user.id)
    else:
        await hellbot.delete(message, "__This user is not a stan!__")


HelpMenu("stan").add(
    "stan",
    None,
    "Get a list of stan users for your client.",
    "stan",
    "A stan user can access some of the commands of your client.",
).add(
    "addstan",
    "<reply/username/userid>",
    "Add a stan user in your client.",
    "addstan",
    "Be careful while adding a stan user.",
).add(
    "delstan",
    "<reply/username/userid>",
    "Remove a stan user from your client.",
    "delstan",
).info(
    "Stan Users"
).done()
