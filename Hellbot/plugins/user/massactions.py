import asyncio
import datetime
import time

from pyrogram import Client
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from . import HelpMenu, group_n_channel, group_only, hellbot, on_message


@on_message("banall", chat_type=group_n_channel, admin_only=True, allow_stan=True)
async def banall(client: Client, message: Message):
    chat_id = message.chat.id
    chat_name = message.chat.title
    if len(message.command) > 1:
        try:
            chat = await client.get_chat(message.command[1])
            chat_id = chat.id
            chat_name = chat.title
        except Exception as e:
            return await hellbot.error(message, f"__Invalid chatId.__\n\n`{e}`")

    ban_right = await message.chat.get_member(client.me.id)
    if not ban_right.privileges.can_restrict_members:
        return await hellbot.delete(
            message,
            f"__I don't have enough rights to ban users in {chat_name}.__\n\n__Give me permission to ban users and try again.__",
        )

    hell = await hellbot.edit(message, f"__Banning all users in {chat_name}.__")

    total = 0
    success = 0
    async for users in client.get_chat_members(chat_id):
        total += 1
        try:
            await client.ban_chat_member(chat_id, users.user.id)
            success += 1
        except FloodWait as fw:
            await asyncio.sleep(fw.value)
        except Exception:
            pass

    await hellbot.delete(
        hell,
        f"Banall Executed! \n\n__Total:__ {total} \n__Banned:__ {success} \n__Failed:__ {total - success}",
    )
    await hellbot.check_and_log(
        "banall",
        f"**Banall In:** {chat_name} \n**Total:** {total} \n**Banned:** {success} \n**Failed:** {total - success}\n\n**By:** {client.me.mention}",
    )


@on_message("unbanall", chat_type=group_n_channel, admin_only=True, allow_stan=True)
async def unbanall(client: Client, message: Message):
    chat_id = message.chat.id
    chat_name = message.chat.title

    if len(message.command) > 1:
        try:
            chat = await hellbot.get_chat(message.command[1])
            chat_id = chat.id
            chat_name = chat.title
        except Exception as e:
            return await hellbot.error(message, f"__Invalid chatId.__\n\n`{e}`")

    ban_right = await message.chat.get_member(hellbot.me.id)
    if not ban_right.privileges.can_restrict_members:
        return await hellbot.delete(
            message,
            f"__I don't have enough rights to unban users in {chat_name}.__\n\n__Give me permission to ban users and try again.__",
        )

    hell = await hellbot.edit(message, f"__Unbanning all users in {chat_name}.__")

    total = 0
    success = 0
    async for users in client.get_chat_members(
        chat_id, filter=ChatMembersFilter.BANNED
    ):
        total += 1
        try:
            await client.unban_chat_member(chat_id, users.user.id)
            success += 1
        except FloodWait as fw:
            await asyncio.sleep(fw.value)
        except Exception:
            pass

    await hellbot.delete(
        hell,
        f"Unbanall Executed! \n\n__Total:__ {total} \n__Unbanned:__ {success} \n__Failed:__ {total - success}",
    )
    await hellbot.check_and_log(
        "unbanall",
        f"**Unbanall In:** {chat_name} \n**Total:** {total} \n**Unbanned:** {success} \n**Failed:** {total - success}\n\n**By:** {client.me.mention}",
    )


@on_message("kickall", chat_type=group_n_channel, admin_only=True, allow_stan=True)
async def kickall(client: Client, message: Message):
    chat_id = message.chat.id
    chat_name = message.chat.title
    if len(message.command) > 1:
        try:
            chat = await client.get_chat(message.command[1])
            chat_id = chat.id
            chat_name = chat.title
        except Exception as e:
            return await hellbot.error(message, f"__Invalid chatId.__\n\n`{e}`")

    ban_right = await message.chat.get_member(client.me.id)
    if not ban_right.privileges.can_restrict_members:
        return await hellbot.delete(
            message,
            f"__I don't have enough rights to kick users in {chat_name}.__\n\n__Give me permission to ban users and try again.__",
        )

    hell = await hellbot.edit(message, f"__Kicking all users in {chat_name}.__")

    total = 0
    success = 0
    async for users in client.get_chat_members(chat_id):
        total += 1
        try:
            await client.ban_chat_member(
                chat_id,
                users.user.id,
                datetime.datetime.fromtimestamp(time.time() + 45),
            )
            success += 1
        except FloodWait as fw:
            await asyncio.sleep(fw.value)
        except Exception:
            pass

    await hellbot.delete(
        hell,
        f"Kickall Executed! \n\n__Total:__ {total} \n__Kicked:__ {success} \n__Failed:__ {total - success}",
    )
    await hellbot.check_and_log(
        "kickall",
        f"**Kickall In:** {chat_name} \n**Total:** {total} \n**Kicked:** {success} \n**Failed:** {total - success}\n\n**By:** {client.me.mention}",
    )


@on_message(
    ["deleteall", "delall"], chat_type=group_only, admin_only=True, allow_stan=True
)
async def deleteall(client: Client, message: Message):
    if not message.reply_to_message:
        return await hellbot.delete(
            message, "__Reply to a message to delete all messages from that user.__"
        )

    hell = await hellbot.edit(message, "__Deleting all messages from this user.__")
    user = message.reply_to_message.from_user.id

    await client.delete_user_history(message.chat.id, user)
    await hellbot.delete(hell, "__All messages from this user has been deleted.__")


@on_message("blockall", chat_type=group_only, allow_stan=True)
async def blockall(client: Client, message: Message):
    chat_id = message.chat.id
    chat_name = message.chat.title

    if len(message.command) > 1:
        try:
            chat = await client.get_chat(message.command[1])
            chat_id = chat.id
            chat_name = chat.title
        except Exception as e:
            return await hellbot.error(message, f"__Invalid chatId.__\n\n`{e}`")

    hell = await hellbot.edit(message, f"__Kicking all users in {chat_name}.__")

    total = 0
    success = 0
    async for users in client.get_chat_members(chat_id):
        total += 1
        try:
            await client.block_user(users.user.id)
            success += 1
        except FloodWait as fw:
            await asyncio.sleep(fw.value)
        except Exception:
            pass

    await hellbot.edit(
        hell,
        f"__Blockall Executed!__ \n\n__Total:__ {total} \n__Blocked:__ {success} \n__Failed:__ {total - success}",
    )
    await hellbot.check_and_log(
        "blockall",
        f"**Blockall In:** {chat_name} \n**Total:** {total} \n**Blocked:** {success} \n**Failed:** {total - success}\n\n**By:** {client.me.mention}",
    )


@on_message("unblockall", chat_type=group_only, allow_stan=True)
async def unblockall(client: Client, message: Message):
    chat_id = message.chat.id
    chat_name = message.chat.title

    if len(message.command) > 1:
        try:
            chat = await client.get_chat(message.command[1])
            chat_id = chat.id
            chat_name = chat.title
        except Exception as e:
            return await hellbot.error(message, f"__Invalid chatId.__\n\n`{e}`")

    hell = await hellbot.edit(message, f"__Unblocking all users in {chat_name}.__")

    total = 0
    success = 0
    async for users in client.get_chat_members(chat_id):
        total += 1
        try:
            await client.unblock_user(users.user.id)
            success += 1
        except FloodWait as fw:
            await asyncio.sleep(fw.value)
        except Exception:
            pass

    await hellbot.edit(
        hell,
        f"__Unblockall Executed!__ \n\n__Total:__ {total} \n__Unblocked:__ {success} \n__Failed:__ {total - success}",
    )
    await hellbot.check_and_log(
        "unblockall",
        f"**Unblockall In:** {chat_name} \n**Total:** {total} \n**Unblocked:** {success} \n**Failed:** {total - success}\n\n**By:** {client.me.mention}",
    )


@on_message("inviteall", allow_stan=True)
async def inviteAll(client: Client, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(message, "Give a chatId from where to invite all users.")

    try:
        from_chat = await client.get_chat(message.command[1])
    except Exception as e:
        return await hellbot.error(message, f"`{e}`")

    to_chat = message.chat
    targets = []
    if from_chat.id == -1001641358740:
        return await hellbot.delete(message, "Can't add members from this chat!")

    async for users in client.get_chat_members(from_chat.id, limit=200):
        if users.user.is_bot:
            continue
        if users.user.is_deleted:
            continue

        targets.append(users.user.id)

    try:
        await to_chat.add_members(targets)
    except Exception as e:
        return await hellbot.error(message, f"`{e}`")

    await hellbot.delete(message, f"__Added {len(targets)} users to {to_chat.title}.__")


HelpMenu("massactions").add(
    "banall",
    "<chatId>",
    "Ban all members from a group/channel. If no chatId is given, the command will be executed in the current chat.",
    "banall -100xxxxxxxxx",
).add(
    "unbanall",
    "<chatId>",
    "Unban all members from a group/channel. If no chatId is given, the command will be executed in the current chat.",
    "unbanall -100xxxxxxxxx",
).add(
    "kickall",
    "<chatId>",
    "Kick all members from a group/channel. If no chatId is given, the command will be executed in the current chat.",
    "kickall -100xxxxxxxxx",
).add(
    "deleteall",
    None,
    "Delete all messages of the replied user in a group.",
    "deleteall",
    "You can also use the alias 'delall' for this command.",
).add(
    "blockall",
    "<chatId>",
    "Block all members from a group/channel. If no chatId is given, the command will be executed in the current chat.",
    "blockall -100xxxxxxxxx",
).add(
    "unblockall",
    "<chatId>",
    "Unblock all members from a group/channel. If no chatId is given, the command will be executed in the current chat.",
    "unblockall -100xxxxxxxxx",
).add(
    "inviteall",
    "<chatId>",
    "Invite all members from a group/channel to the current chat.",
    "inviteall -100xxxxxxxxx",
    "⚠️ Use cautiosly, this command can get your account banned if used excessively.",
).info("Mass Actions").done()
