import asyncio

from pyrogram import Client
from pyrogram.types import ChatPermissions, ChatPrivileges, Message

from Hellbot.core import LOGS

from . import HelpMenu, group_only, handler, hellbot, on_message


@on_message(
    "promote",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
)
async def promote(client: Client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await hellbot.delete(
            message, "𝖭𝖾𝖾𝖽 𝖺 𝗎𝗌𝖾𝗋𝗇𝖺𝗆𝖾/𝗂𝖽 𝗈𝗋 𝗋𝖾𝗉𝗅𝗒 𝗍𝗈 𝖺 𝗎𝗌𝖾𝗋 𝗍𝗈 𝗉𝗋𝗈𝗆𝗈𝗍𝖾 𝗍𝗁𝖾𝗆!"
        )

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        title = await hellbot.input(message)
    else:
        user = await client.get_users(message.command[1])
        title = (await hellbot.input(message)).split(" ", 1)[1].strip() or ""

    try:
        privileges = ChatPrivileges(
            can_manage_chat=True,
            can_delete_messages=True,
            can_manage_video_chats=True,
            can_restrict_members=False,
            can_promote_members=False,
            can_change_info=False,
            can_invite_users=True,
            can_pin_messages=True,
            is_anonymous=False,
        )
        await message.chat.promote_member(user.id, privileges)
        await client.set_administrator_title(message.chat.id, user.id, title)
    except Exception as e:
        return await hellbot.error(message, e)

    await hellbot.delete(message, f"**💫 𝖯𝗋𝗈𝗆𝗈𝗍𝖾𝖽 {user.mention} 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒!**")
    await hellbot.check_and_log(
        "promote",
        f"**Promoted User**\n\n**User:** {user.mention}\n**User ID:** `{user.id}`\n**Admin:** `{message.from_user.mention}`\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "demote",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
)
async def demote(client: Client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await hellbot.delete(
            message, "𝖭𝖾𝖾𝖽 𝖺 𝗎𝗌𝖾𝗋𝗇𝖺𝗆𝖾/𝗂𝖽 𝗈𝗋 𝗋𝖾𝗉𝗅𝗒 𝗍𝗈 𝖺 𝗎𝗌𝖾𝗋 𝗍𝗈 𝖽𝖾𝗆𝗈𝗍𝖾 𝗍𝗁𝖾𝗆!"
        )

    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        user = await client.get_users(message.command[1])
    try:
        privileges = ChatPrivileges(
            can_manage_chat=False,
            can_delete_messages=False,
            can_manage_video_chats=False,
            can_restrict_members=False,
            can_promote_members=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
            is_anonymous=False,
        )
        await message.chat.promote_member(user.id, privileges)
    except Exception as e:
        return await hellbot.error(message, e)

    await hellbot.delete(message, f"**🙄 𝖣𝖾𝗆𝗈𝗍𝖾𝖽 {user.mention} 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒!**")
    await hellbot.check_and_log(
        "demote",
        f"**Demoted User**\n\n**User:** {user.mention}\n**User ID:** `{user.id}`\n**Admin:** `{message.from_user.mention}`\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "ban",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
)
async def ban(client: Client, message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        if len(message.command) < 2:
            reason = None
        else:
            reason = await hellbot.input(message)
    elif len(message.command) == 2:
        user = await client.get_users(message.command[1])
        reason = None
    elif len(message.command) > 2:
        user = await client.get_users(message.command[1])
        reason = (await hellbot.input(message)).split(" ", 1)[1].strip()
    else:
        return await hellbot.delete(
            message, "𝖭𝖾𝖾𝖽 𝖺 𝗎𝗌𝖾𝗋𝗇𝖺𝗆𝖾/𝗂𝖽 𝗈𝗋 𝗋𝖾𝗉𝗅𝗒 𝗍𝗈 𝖺 𝗎𝗌𝖾𝗋 𝗍𝗈 𝖻𝖺𝗇 𝗍𝗁𝖾𝗆!"
        )

    try:
        await message.chat.ban_member(user.id)
    except Exception as e:
        return await hellbot.error(message, e)

    reason = reason if reason else "Not Specified"
    await hellbot.delete(
        message,
        f"**☠️ 𝖡𝖺𝗇𝗇𝖾𝖽 {user.mention} 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒!**\n**𝖱𝖾𝖺𝗌𝗈𝗇:** `{reason}`",
        30,
    )
    await hellbot.check_and_log(
        "ban",
        f"**Banned User**\n\n**User:** {user.mention}\n**User ID:** `{user.id}`\n**Reason:** `{reason}`\n**Admin:** `{message.from_user.mention}`\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "unban",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
)
async def unban(client: Client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await hellbot.delete(
            message, "𝖭𝖾𝖾𝖽 𝖺 𝗎𝗌𝖾𝗋𝗇𝖺𝗆𝖾/𝗂𝖽 𝗈𝗋 𝗋𝖾𝗉𝗅𝗒 𝗍𝗈 𝖺 𝗎𝗌𝖾𝗋 𝗍𝗈 𝗎𝗇𝖻𝖺𝗇 𝗍𝗁𝖾𝗆!"
        )

    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        user = await client.get_users(message.command[1])

    try:
        await message.chat.unban_member(user.id)
    except Exception as e:
        return await hellbot.error(message, e)

    await hellbot.delete(message, f"**🤗 𝖴𝗇𝖻𝖺𝗇𝗇𝖾𝖽 {user.mention} 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒!**", 30)
    await hellbot.check_and_log(
        "unban",
        f"**Unbanned User**\n\n**User:** {user.mention}\n**User ID:** `{user.id}`\n**Admin:** `{message.from_user.mention}`\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "kick",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
)
async def kick(client: Client, message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        if len(message.command) < 2:
            reason = None
        else:
            reason = await hellbot.input(message)
    elif len(message.command) == 2:
        user = await client.get_users(message.command[1])
        reason = None
    elif len(message.command) > 2:
        user = await client.get_users(message.command[1])
        reason = (await hellbot.input(message)).split(" ", 1)[1].strip()
    else:
        return await hellbot.delete(
            message, "𝖭𝖾𝖾𝖽 𝖺 𝗎𝗌𝖾𝗋𝗇𝖺𝗆𝖾/𝗂𝖽 𝗈𝗋 𝗋𝖾𝗉𝗅𝗒 𝗍𝗈 𝖺 𝗎𝗌𝖾𝗋 𝗍𝗈 𝗄𝗂𝖼𝗄 𝗍𝗁𝖾𝗆!"
        )

    try:
        await message.chat.ban_member(user.id)
    except Exception as e:
        return await hellbot.error(message, e)

    reason = reason if reason else "Not Specified"
    await hellbot.delete(
        message,
        f"**👋 𝖪𝗂𝖼𝗄𝖾𝖽 {user.mention} 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒!**\n**𝖱𝖾𝖺𝗌𝗈𝗇:** `{reason}`",
        30,
    )
    await hellbot.check_and_log(
        "kick",
        f"**Kicked User**\n\n**User:** {user.mention}\n**User ID:** `{user.id}`\n**Reason:** `{reason}`\n**Admin:** `{message.from_user.mention}`\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )
    await asyncio.sleep(5)
    await message.chat.unban_member(user.id)


@on_message(
    "mute",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
)
async def mute(client: Client, message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        if len(message.command) < 2:
            reason = None
        else:
            reason = await hellbot.input(message)
    elif len(message.command) == 2:
        user = await client.get_users(message.command[1])
        reason = None
    elif len(message.command) > 2:
        user = await client.get_users(message.command[1])
        reason = (await hellbot.input(message)).split(" ", 1)[1].strip()
    else:
        return await hellbot.delete(
            message, "𝖭𝖾𝖾𝖽 𝖺 𝗎𝗌𝖾𝗋𝗇𝖺𝗆𝖾/𝗂𝖽 𝗈𝗋 𝗋𝖾𝗉𝗅𝗒 𝗍𝗈 𝖺 𝗎𝗌𝖾𝗋 𝗍𝗈 𝗆𝗎𝗍𝖾 𝗍𝗁𝖾𝗆!"
        )

    try:
        permissions = ChatPermissions(
            can_send_messages=False,
        )
        await message.chat.restrict_member(user.id, permissions)
    except Exception as e:
        return await hellbot.error(message, e)

    reason = reason if reason else "Not Specified"
    await hellbot.delete(
        message, f"**🤐 𝖬𝗎𝗍𝖾𝖽 {user.mention} 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒!**\n**𝖱𝖾𝖺𝗌𝗈𝗇:** `{reason}`", 30
    )
    await hellbot.check_and_log(
        "mute",
        f"**Muted User**\n\n**User:** {user.mention}\n**User ID:** `{user.id}`\n**Reason:** `{reason}`\n**Admin:** `{message.from_user.mention}`\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "unmute",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
)
async def unmute(client: Client, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await hellbot.delete(
            message, "𝖭𝖾𝖾𝖽 𝖺 𝗎𝗌𝖾𝗋𝗇𝖺𝗆𝖾/𝗂𝖽 𝗈𝗋 𝗋𝖾𝗉𝗅𝗒 𝗍𝗈 𝖺 𝗎𝗌𝖾𝗋 𝗍𝗈 𝗎𝗇𝗆𝗎𝗍𝖾 𝗍𝗁𝖾𝗆!"
        )

    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        user = await client.get_users(message.command[1])

    try:
        permissions = ChatPermissions(
            can_send_messages=True,
        )
        await message.chat.restrict_member(user.id, permissions)
    except Exception as e:
        return await hellbot.error(message, e)

    await hellbot.delete(message, f"**😁 𝖴𝗇𝗆𝗎𝗍𝖾𝖽 {user.mention} 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒!**", 30)
    await hellbot.check_and_log(
        "unmute",
        f"**Unmuted User**\n\n**User:** {user.mention}\n**User ID:** `{user.id}`\n**Admin:** `{message.from_user.mention}`\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "pin",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
)
async def pin(_, message: Message):
    if not message.reply_to_message:
        return await hellbot.delete(message, "𝖭𝖾𝖾𝖽 𝖺 𝗋𝖾𝗉𝗅𝗒 𝗍𝗈 𝗉𝗂𝗇 𝖺 𝗆𝖾𝗌𝗌𝖺𝗀𝖾!")

    try:
        await message.reply_to_message.pin()
    except Exception as e:
        return await hellbot.error(message, e)

    await hellbot.delete(
        message,
        f"**📌 𝖯𝗂𝗇𝗇𝖾𝖽 [𝖬𝖾𝗌𝗌𝖺𝗀𝖾]({message.reply_to_message.link}) 𝗂𝗇 {message.chat.title}!**",
        30,
    )
    await hellbot.check_and_log(
        "pin",
        f"**Pinned Message**\n\n**Message:** [Click Here]({message.reply_to_message.link})\n**Admin:** `{message.from_user.mention}`\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "unpin",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
)
async def unpin(_, message: Message):
    if not message.reply_to_message:
        return await hellbot.delete(message, "𝖭𝖾𝖾𝖽 𝖺 𝗋𝖾𝗉𝗅𝗒 𝗍𝗈 𝗎𝗇𝗉𝗂𝗇 𝖺 𝗆𝖾𝗌𝗌𝖺𝗀𝖾!")

    try:
        await message.reply_to_message.unpin()
    except Exception as e:
        return await hellbot.error(message, e)

    await hellbot.delete(
        message,
        f"**📌 𝖴𝗇𝗉𝗂𝗇𝗇𝖾𝖽 [𝖬𝖾𝗌𝗌𝖺𝗀𝖾]({message.reply_to_message.link}) 𝗂𝗇 {message.chat.title}!**",
        30,
    )
    await hellbot.check_and_log(
        "unpin",
        f"**Unpinned Message**\n\n**Message:** [Click Here]({message.reply_to_message.link})\n**Admin:** `{message.from_user.mention}`\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`",
    )


@on_message(
    "zombies",
    chat_type=group_only,
    admin_only=True,
    allow_stan=True,
)
async def zombies(_, message: Message):
    hell = await hellbot.edit(message, "☠️ 𝖣𝖾𝗍𝖾𝖼𝗍𝗂𝗇𝗀 𝗓𝗈𝗆𝖻𝗂𝖾𝗌...")
    ded_users = []
    async for members in message.chat.get_members():
        if members.user.is_deleted:
            ded_users.append(members.user.id)

    if not ded_users:
        return await hell.edit(
            "🫡 𝖣𝗈𝗇'𝗍 𝗁𝖺𝗏𝖾 𝖺𝗇𝗒 𝗓𝗈𝗆𝖻𝗂𝖾𝗌 𝗂𝗇 𝗍𝗁𝗂𝗌 𝗀𝗋𝗈𝗎𝗉. **𝖦𝗋𝗈𝗎𝗉𝗌' 𝖼𝗅𝖾𝖺𝗇 𝖠𝖥!**"
        )

    if len(message.command) > 1 and message.command[1].lower() == "clean":
        await hell.edit(
            f"☠️ 𝖥𝗈𝗎𝗇𝖽 {len(ded_users)} 𝗓𝗈𝗆𝖻𝗂𝖾𝗌... **🔫 𝖳𝗂𝗆𝖾 𝗍𝗈 𝗉𝗎𝗋𝗀𝖾 𝗍𝗁𝖾𝗆!**"
        )
        failed = 0
        success = 0
        for user in ded_users:
            try:
                await message.chat.ban_member(user)
                success += 1
            except Exception as e:
                LOGS.error(e)
                failed += 1

        await hell.edit(f"**𝖯𝗎𝗋𝗀𝖾𝖽 {success} 𝗓𝗈𝗆𝖻𝗂𝖾𝗌!**\n`{failed}` holds immunity!")
    else:
        await hell.edit(
            f"**☠️ 𝖥𝗈𝗎𝗇𝖽 {len(ded_users)} 𝗓𝗈𝗆𝖻𝗂𝖾𝗌!**\n\n__Use__ `{handler}zombies clean` __to kill them!__"
        )


HelpMenu("admin").add(
    "promote", "<𝗎𝗌𝖾𝗋𝗇𝖺𝗆𝖾/𝗂𝖽/reply> <𝗍𝗂𝗍𝗅𝖾>", "Promote a user to admin.", "promote @ForGo10God hellboy"
).add(
    "demote", "<username/id/reply>", "Demote a user from admin.", "demote @ForGo10God"
).add(
    "ban", "<username/id/reply> <reason>", "Ban a user from the group.", "ban @ForGo10God"
).add(
    "unban", "<username/id/reply>", "Unban a user from the group.", "unban @ForGo10God"
).add(
    "kick", "<username/id/reply> <reason>", "Kick a user from the group.", "kick @ForGo10God"
).add(
    "mute", "<username/id/reply> <reason>", "Mute a user in the group", "mute @ForGo10God"
).add(
    "unmute", "<username/id/reply>", "Unmute a user in the group.", "unmute @ForGo10God"
).add(
    "pin", "<reply>", "Pin the replied message in the group."
).add(
    "unpin", "<reply>", "Unpin the replied pinned message in the group."
).add(
    "zombies", "clean", "Finds the total number of deleted users present in that group and ban them."
).info("Admin Menu").done()
