import asyncio
import datetime

from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait
from pyrogram.types import ChatPermissions, ChatPrivileges, Message

from Hellbot.functions.templates import gban_templates

from . import Config, HelpMenu, Symbols, custom_handler, db, hellbot, on_message


@on_message("gpromote", allow_stan=True)
async def globalpromote(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            return await hellbot.delete(
                message, "Reply to a user or pass a username/id to gpromote."
            )
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await hellbot.error(message, f"`{str(e)}`")
        reason = (
            message.text.split(None, 2)[2]
            if len(message.text.split()) > 2
            else "No reason provided."
        )
    else:
        user = message.reply_to_message.from_user
        reason = await hellbot.input(message) or "No reason provided."

    if user.is_self:
        return await hellbot.delete(message, "I can't gpromote myself.")

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

    success = 0
    failed = 0
    hell = await hellbot.edit(message, f"Gpromote initiated on {user.mention}...")

    async for dialog in client.get_dialogs:
        if dialog.chat.type in [
            ChatType.CHANNEL,
            ChatType.GROUP,
            ChatType.SUPERGROUP,
        ]:
            try:
                await dialog.chat.promote_member(user.id, privileges)
                success += 1
            except FloodWait as e:
                await hell.edit(
                    f"Gpromote initiated on {user.mention}...\nSleeping for {e.x} seconds due to floodwait..."
                )
                await asyncio.sleep(e.x)
                await dialog.chat.ban_member(user.id)
                success += 1
                await hell.edit(f"Gpromote initiated on {user.mention}...")
            except BaseException:
                failed += 1

    await hell.edit(
        await gban_templates(
            gtype="𝖦-𝖯𝗋𝗈𝗆𝗈𝗍𝖾",
            name=user.mention,
            success=success,
            failed=failed,
            reason=reason,
        )
    )

    await hellbot.check_and_log(
        "gpromote",
        f"**User:** {user.mention} (`{user.id}`)\n**By: {client.me.mention}**\n\n**Reason:** `{reason}`",
    )


@on_message("gdemote", allow_stan=True)
async def globaldemote(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            return await hellbot.delete(
                message, "Reply to a user or pass a username/id to gdemote."
            )
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await hellbot.error(message, f"`{str(e)}`")
        reason = (
            message.text.split(None, 2)[2]
            if len(message.text.split()) > 2
            else "No reason provided."
        )
    else:
        user = message.reply_to_message.from_user
        reason = await hellbot.input(message) or "No reason provided."

    if user.is_self:
        return await hellbot.delete(message, "I can't gdemote myself.")

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

    success = 0
    failed = 0
    hell = await hellbot.edit(message, f"Gdemote initiated on {user.mention}...")

    async for dialog in client.get_dialogs:
        if dialog.chat.type in [
            ChatType.CHANNEL,
            ChatType.GROUP,
            ChatType.SUPERGROUP,
        ]:
            try:
                await dialog.chat.promote_member(user.id, privileges)
                success += 1
            except FloodWait as e:
                await hell.edit(
                    f"Gdemote initiated on {user.mention}...\nSleeping for {e.x} seconds due to floodwait..."
                )
                await asyncio.sleep(e.x)
                await dialog.chat.ban_member(user.id)
                success += 1
                await hell.edit(f"Gdemote initiated on {user.mention}...")
            except BaseException:
                failed += 1

    await hell.edit(
        await gban_templates(
            gtype="𝖦-𝖣𝖾𝗆𝗈𝗍𝖾",
            name=user.mention,
            success=success,
            failed=failed,
            reason=reason,
        )
    )

    await hellbot.check_and_log(
        "gdemote",
        f"**User:** {user.mention} (`{user.id}`)\n**By: {client.me.mention}**\n\n**Reason:** `{reason}`",
    )


@on_message("gban", allow_stan=True)
async def globalban(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            return await hellbot.delete(
                message, "Reply to a user or pass a username/id to gban."
            )
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await hellbot.error(message, f"`{str(e)}`")
        reason = (
            message.text.split(None, 2)[2]
            if len(message.text.split()) > 2
            else "No reason provided."
        )
    else:
        user = message.reply_to_message.from_user
        reason = await hellbot.input(message) or "No reason provided."

    if user.is_self:
        return await hellbot.delete(message, "I can't gban myself.")

    if user.id in Config.AUTH_USERS:
        return await hellbot.delete(message, "I can't gban my auth user.")

    if user.id in Config.BANNED_USERS:
        return await hellbot.delete(message, "This user is already gbanned.")

    if user.id in Config.DEVS:
        return await hellbot.delete(message, "I can't gban my devs.")

    success = 0
    failed = 0
    hell = await hellbot.edit(message, f"Gban initiated on {user.mention}...")

    await db.add_gban(user.id, reason)
    Config.BANNED_USERS.add(user.id)

    async for dialog in client.get_dialogs():
        if dialog.chat.type in [
            ChatType.CHANNEL,
            ChatType.GROUP,
            ChatType.SUPERGROUP,
        ]:
            try:
                await dialog.chat.ban_member(user.id)
                success += 1
            except FloodWait as e:
                await hell.edit(
                    f"Gban initiated on {user.mention}...\nSleeping for {e.x} seconds due to floodwait..."
                )
                await asyncio.sleep(e.x)
                await dialog.chat.ban_member(user.id)
                success += 1
                await hell.edit(f"Gban initiated on {user.mention}...")
            except BaseException:
                failed += 1

    await hell.edit(
        await gban_templates(
            gtype="𝖦-𝖡𝖺𝗇",
            name=user.mention,
            success=success,
            failed=failed,
            reason=reason,
        )
    )

    await hellbot.check_and_log(
        "gban",
        f"**User:** {user.mention} (`{user.id}`)\n**By: {client.me.mention}**\n\n**Reason:** `{reason}`",
    )


@on_message("ungban", allow_stan=True)
async def unglobalban(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            return await hellbot.delete(
                message, "Reply to a user or pass a username/id to ungban."
            )
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await hellbot.error(message, f"`{str(e)}`")
    else:
        user = message.reply_to_message.from_user

    if user.id not in Config.BANNED_USERS:
        await hellbot.delete(
            message,
            "This user is not gbanned. Unbanning in all my admin chats anyway...",
        )
    else:
        reason = await db.rm_gban(user.id)
        Config.BANNED_USERS.remove(user.id)
        await hellbot.edit(
            message,
            f"**𝖴𝗇𝗀𝖻𝖺𝗇𝗇𝖾𝖽** {user.mention}!\n\n**𝖦𝖻𝖺𝗇 𝖱𝖾𝖺𝗌𝗈𝗇 𝗐𝖺𝗌:** `{reason}`",
        )

    async for dialog in client.get_dialogs():
        if dialog.chat.type in [
            ChatType.CHANNEL,
            ChatType.GROUP,
            ChatType.SUPERGROUP,
        ]:
            try:
                await dialog.chat.unban_member(user.id)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await dialog.chat.unban_member(user.id)
            except BaseException:
                pass

    await hellbot.check_and_log(
        "ungban",
        f"**User:** {user.mention} (`{user.id}`)\n**By: {message.from_user.mention}**",
    )


@on_message("gkick", allow_stan=True)
async def globalkick(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            return await hellbot.delete(
                message, "Reply to a user or pass a username/id to gkick."
            )
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await hellbot.error(message, f"`{str(e)}`")
        reason = (
            message.text.split(None, 2)[2]
            if len(message.text.split()) > 2
            else "No reason provided."
        )
    else:
        user = message.reply_to_message.from_user
        reason = await hellbot.input(message) or "No reason provided."

    if user.is_self:
        return await hellbot.delete(message, "I can't gkick myself.")

    if user.id in Config.AUTH_USERS:
        return await hellbot.delete(message, "I can't gkick my auth user.")

    if user.id in Config.BANNED_USERS:
        return await hellbot.delete(
            message, "This user is already gbanned. There's no point in kicking them!"
        )

    if user.id in Config.DEVS:
        return await hellbot.delete(message, "I can't gkick my devs.")

    success = 0
    failed = 0
    hell = await hellbot.edit(message, f"Gkick initiated on {user.mention}...")

    async for dialog in client.get_dialogs():
        if dialog.chat.type in [
            ChatType.CHANNEL,
            ChatType.GROUP,
            ChatType.SUPERGROUP,
        ]:
            try:
                await dialog.chat.ban_member(
                    user.id, datetime.datetime.now() + datetime.timedelta(seconds=35)
                )
                success += 1
            except FloodWait as e:
                await hell.edit(
                    f"Gkick initiated on {user.mention}...\nSleeping for {e.x} seconds due to floodwait..."
                )
                await asyncio.sleep(e.x)
                await dialog.chat.ban_member(
                    user.id, datetime.datetime.now() + datetime.timedelta(seconds=35)
                )
                success += 1
                await hell.edit(f"Gkick initiated on {user.mention}...")
            except BaseException:
                failed += 1

    await hell.edit(
        await gban_templates(
            gtype="𝖦-𝖪𝗂𝖼𝗄",
            name=user.mention,
            success=success,
            failed=failed,
            reason=reason,
        )
    )

    await hellbot.check_and_log(
        "gkick",
        f"**User:** {user.mention} (`{user.id}`)\n**By: {client.me.mention}**\n\n**Reason:** `{reason}`",
    )


@on_message("gmute", allow_stan=True)
async def globalmute(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            return await hellbot.delete(
                message, "Reply to a user or pass a username/id to gmute."
            )
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await hellbot.error(message, f"`{str(e)}`")
        reason = (
            message.text.split(None, 2)[2]
            if len(message.text.split()) > 2
            else "No reason provided."
        )
    else:
        user = message.reply_to_message.from_user
        reason = await hellbot.input(message) or "No reason provided."

    if user.is_self:
        return await hellbot.delete(message, "I can't gkick myself.")

    if user.id in Config.AUTH_USERS:
        return await hellbot.delete(message, "I can't gkick my auth user.")

    if user.id in Config.MUTED_USERS:
        return await hellbot.delete(message, "This user is already gmuted.")

    if user.id in Config.DEVS:
        return await hellbot.delete(message, "I can't gmute my devs.")

    permissions = ChatPermissions(can_send_messages=False)
    success = 0
    failed = 0
    hell = await hellbot.edit(message, f"Gmute initiated on {user.mention}...")

    await db.add_gmute(user.id, reason)
    Config.MUTED_USERS.add(user.id)

    async for dialog in client.get_dialogs():
        if dialog.chat.type in [
            ChatType.CHANNEL,
            ChatType.GROUP,
            ChatType.SUPERGROUP,
        ]:
            try:
                await dialog.chat.restrict_member(user.id, permissions)
                success += 1
            except FloodWait as e:
                await hell.edit(
                    f"Gmute initiated on {user.mention}...\nSleeping for {e.x} seconds due to floodwait..."
                )
                await asyncio.sleep(e.x)
                await dialog.chat.restrict_member(user.id, permissions)
                success += 1
                await hell.edit(f"Gmute initiated on {user.mention}...")
            except BaseException:
                failed += 1

    await hell.edit(
        await gban_templates(
            gtype="𝖦-𝖬𝗎𝗍𝖾",
            name=user.mention,
            success=success,
            failed=failed,
            reason=reason,
        )
    )

    await hellbot.check_and_log(
        "gmute",
        f"**User:** {user.mention} (`{user.id}`)\n**By: {client.me.mention}**\n\n**Reason:** `{reason}`",
    )


@on_message("ungmute", allow_stan=True)
async def unglobalmute(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            return await hellbot.delete(
                message, "Reply to a user or pass a username/id to ungmute."
            )
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await hellbot.error(message, f"`{str(e)}`")
    else:
        user = message.reply_to_message.from_user

    if user.id not in Config.MUTED_USERS:
        await hellbot.delete(
            message, "This user is not gmuted. Unmuting in all my admin chats anyway..."
        )
    else:
        reason = await db.rm_gmute(user.id)
        Config.MUTED_USERS.remove(user.id)
        await hellbot.edit(
            message,
            f"**𝖴𝗇𝗀𝗆𝗎𝗍𝖾𝖽** {user.mention}!\n\n**𝖦𝗆𝗎𝗍𝖾 𝖱𝖾𝖺𝗌𝗈𝗇 𝗐𝖺𝗌:** `{reason}`",
        )

    permissions = ChatPermissions(can_send_messages=True)

    async for dialog in client.get_dialogs():
        if dialog.chat.type in [
            ChatType.CHANNEL,
            ChatType.GROUP,
            ChatType.SUPERGROUP,
        ]:
            try:
                await dialog.chat.restrict_member(user.id, permissions)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await dialog.chat.restrict_member(user.id, permissions)
            except BaseException:
                pass

    await hellbot.check_and_log(
        "ungmute",
        f"**User:** {user.mention} (`{user.id}`)\n**By: {message.from_user.mention}**",
    )


@on_message("gbanlist", allow_stan=True)
async def gbanlist(_, message: Message):
    gban_users = await db.get_gban()
    if not gban_users:
        return await hellbot.delete(message, "No gbanned users.")

    hell = await hellbot.edit(message, "Fetching gbanned users...")
    text = f"**💥 𝖦𝖻𝖺𝗇𝗇𝖾𝖽 𝖴𝗌𝖾𝗋𝗌:** __{len(gban_users)}__\n\n"

    for user in gban_users:
        text += f"{Symbols.bullet} `{user['user_id']}` | __{user['reason']}__\n\n"

    await hell.edit(text)


@on_message("gmutelist", allow_stan=True)
async def gmutelist(_, message: Message):
    gmute_users = await db.get_gmute()
    if not gmute_users:
        return await hellbot.delete(message, "No gmuted users.")

    hell = await hellbot.edit(message, "Fetching gmuted users...")
    text = f"**😶 𝖦𝗆𝗎𝗍𝖾𝖽 𝖴𝗌𝖾𝗋𝗌:** __{len(gmute_users)}__\n\n"

    for user in gmute_users:
        text += f"{Symbols.bullet} `{user['user_id']}` | __{user['reason']}__\n\n"

    await hell.edit(text)


@custom_handler(filters.incoming & ~filters.service)
async def globalmutewatcher(_, message: Message):
    if not message.from_user:
        return

    if await db.is_gmuted(message.from_user.id):
        await message.delete()


@custom_handler(filters.new_chat_members)
async def globalbanwatcher(_, message: Message):
    if not message.from_user:
        return

    if await db.is_gbanned(message.from_user.id):
        gban_data = await db.get_gban_user(message.from_user.id)
        watchertext = f"**𝖦𝖻𝖺𝗇𝗇𝖾𝖽 𝖴𝗌𝖾𝗋 𝗃𝗈𝗂𝗇𝖾𝖽 𝗍𝗁𝖾 𝖼𝗁𝖺𝗍! \n\n{Symbols.bullet} 𝖦𝖻𝖺𝗇 𝖱𝖾𝖺𝗌𝗈𝗇 𝗐𝖺𝗌:** __{gban_data['reason']}__\n**{Symbols.bullet} 𝖦𝖻𝖺𝗇 𝖣𝖺𝗍𝖾:** __{gban_data['date']}__\n\n"

        try:
            await message.chat.ban_member(message.from_user.id)
            watchertext += f"**𝖲𝗈𝗋𝗋𝗒 𝖨 𝖼𝖺𝗇'𝗍 𝗌𝖾𝖾 𝗒𝗈𝗎 𝗂𝗇 𝗍𝗁𝗂𝗌 𝖼𝗁𝖺𝗍!**"
        except BaseException:
            watchertext += f"Reported to @admins"

        await message.reply_text(watchertext)


HelpMenu("superpowers").add(
    "gpromote",
    "<reply/username/id> <reason (optional)>",
    "Promote a user in all the chats where you have add admin right.",
    "gpromote @ForGo10God Why not?",
).add(
    "gdemote",
    "<reply/username/id> <reason (optional)>",
    "Demotes a user in all the chats where you are on top level from the user.",
    "gdemote @ForGo10God Why?",
).add(
    "gban",
    "<reply/username/id> <reason (optional)>",
    "Ban a user in all the chats where you have ban rights.",
    "gban @ForGo10God :)",
).add(
    "ungban",
    "<reply/username/id>",
    "Unban a user in all the chats where you have ban rights.",
    "ungban @ForGo10God",
).add(
    "gkick",
    "<reply/username/id> <reason (optional)>",
    "Kick a user in all the chats where you have ban rights.",
    "gkick @ForGo10God :)",
).add(
    "gmute",
    "<reply/username/id> <reason (optional)>",
    "Mute a user in all the chats where you have mute rights.",
    "gmute @ForGo10God :)",
).add(
    "ungmute",
    "<reply/username/id>",
    "Unmute a user in all the chats where you have mute rights.",
    "ungmute @ForGo10God",
).add(
    "gbanlist", None, "List all the gbanned users.", "gbanlist"
).add(
    "gmutelist", None, "List all the gmuted users.", "gmutelist"
).info(
    "Grants you superpowers!"
).done()
