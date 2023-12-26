import time

from pyrogram import Client
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.raw.functions.channels import GetAdminedPublicChannels
from pyrogram.raw.functions.users import GetFullUser
from pyrogram.types import Message

from Hellbot.functions.formatter import readable_time
from Hellbot.functions.templates import statistics_templates, user_info_templates

from . import HelpMenu, Symbols, hellbot, on_message


@on_message("count", allow_stan=True)
async def count_stats(client: Client, message: Message):
    hell = await hellbot.edit(message, "Processing...")
    bots = 0
    users = 0
    groups = 0
    channels = 0
    super_groups = 0

    async for dialog in client.get_dialogs():
        if dialog.chat.type == ChatType.BOT:
            bots += 1
        elif dialog.chat.type == ChatType.PRIVATE:
            users += 1
        elif dialog.chat.type == ChatType.GROUP:
            groups += 1
        elif dialog.chat.type == ChatType.SUPERGROUP:
            super_groups += 1
        elif dialog.chat.type == ChatType.CHANNEL:
            channels += 1
        else:
            pass

    total = bots + users + groups + super_groups + channels
    await hell.edit(
        f"**{client.me.mention}'𝗌 𝖼𝗁𝖺𝗍𝗌 𝖼𝗈𝗎𝗇𝗍:**\n\n"
        f"    **{Symbols.anchor} 𝖯𝗋𝗂𝗏𝖺𝗍𝖾:** `{users}`\n"
        f"    **{Symbols.anchor} 𝖦𝗋𝗈𝗎𝗉𝗌:** `{groups}`\n"
        f"    **{Symbols.anchor} 𝖲𝗎𝗉𝖾𝗋𝖦𝗋𝗈𝗎𝗉𝗌:** `{super_groups}`\n"
        f"    **{Symbols.anchor} 𝖢𝗁𝖺𝗇𝗇𝖾𝗅𝗌:** `{channels}`\n"
        f"    **{Symbols.anchor} 𝖡𝗈𝗍𝗌:** `{bots}`\n\n"
        f"**{Symbols.triangle_right} 𝖳𝗈𝗍𝖺𝗅:** `{total}`\n"
    )


@on_message("stats", allow_stan=True)
async def mystats(client: Client, message: Message):
    hell = await hellbot.edit(message, "Processing...")
    bots = 0
    ch_admin = 0
    ch_owner = 0
    channels = 0
    gc_admin = 0
    gc_owner = 0
    groups = 0
    unread_mention = 0
    unread_msg = 0
    users = 0

    start = time.time()
    async for dialog in client.get_dialogs():
        if dialog.chat.type == ChatType.CHANNEL:
            meInChat = await dialog.chat.get_member(client.me.id)
            channels += 1
            if meInChat.status == ChatMemberStatus.OWNER:
                ch_owner += 1
            elif meInChat.status == ChatMemberStatus.ADMINISTRATOR:
                ch_admin += 1

        elif dialog.chat.type == ChatType.GROUP:
            meInChat = await dialog.chat.get_member(client.me.id)
            groups += 1
            if meInChat.status == ChatMemberStatus.OWNER:
                gc_owner += 1
            elif meInChat.status == ChatMemberStatus.ADMINISTRATOR:
                gc_admin += 1

        elif dialog.chat.type == ChatType.SUPERGROUP:
            meInChat = await dialog.chat.get_member(client.me.id)
            groups += 1
            if meInChat.status == ChatMemberStatus.OWNER:
                gc_owner += 1
            elif meInChat.status == ChatMemberStatus.ADMINISTRATOR:
                gc_admin += 1

        elif dialog.chat.type == ChatType.PRIVATE:
            users += 1

        elif dialog.chat.type == ChatType.BOT:
            bots += 1

        unread_mention += dialog.unread_mentions_count
        unread_msg += dialog.unread_messages_count

    time_taken = readable_time(int(time.time() - start)) or "0 seconds"

    await hell.edit(
        await statistics_templates(
            name=client.me.mention,
            channels=channels,
            ch_admin=ch_admin,
            ch_owner=ch_owner,
            groups=groups,
            gc_admin=gc_admin,
            gc_owner=gc_owner,
            users=users,
            bots=bots,
            unread_msg=unread_msg,
            unread_mention=unread_mention,
            time_taken=time_taken,
        )
    )


@on_message("reserved", allow_stan=True)
async def reserved(client: Client, message: Message):
    hell = await hellbot.edit(message, "Processing...")
    result = await client.invoke(GetAdminedPublicChannels())

    outStr = f"🍀 **{client.me.mention}'𝗌 𝗋𝖾𝗌𝖾𝗋𝗏𝖾𝖽 𝗎𝗌𝖾𝗋𝗇𝖺𝗆𝖾𝗌:**\n\n"
    for chat in result.chats:
        f"  {Symbols.bullet} {chat.title} - **{chat.username}**\n"

    await hell.edit(outStr)


@on_message("info", allow_stan=True)
async def userInfo(client: Client, message: Message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            return await hellbot.error(message, "Reply to a user or give username/id to get their info.")
        try:
            user = await client.get_users(message.command[1])
        except Exception as e:
            return await hellbot.error(message, str(e))
    else:
        user = message.reply_to_message.from_user

    hell = await hellbot.edit(message, f"Getting info of {user.mention}...")

    try:
        resolved = await client.resolve_peer(user.id)
        fullUser = await client.invoke(GetFullUser(id=resolved))
        bio = fullUser.about
    except:
        bio = None

    total_pfp = await client.get_chat_photos_count(user.id)
    common_chats = len(await user.get_common_chats())

    user_info = await user_info_templates(
        mention=user.mention,
        firstName=user.first_name,
        lastName=user.last_name,
        userId=user.id,
        bio=bio,
        dcId=user.dc_id,
        totalPictures=total_pfp,
        isRestricted=user.is_restricted,
        isVerified=user.is_verified,
        isBot=user.is_bot,
        commonGroups=common_chats,
    )

    if user.photo:
        async for photo in client.get_chat_photos(user.id, 1):
            await hell.delete()
            await client.send_photo(
                message.chat.id,
                photo.file_id,
                caption=user_info,
                reply_to_message_id=message.id,
                disable_notification=True,
            )
            return
    else:
        await hell.edit(user_info, disable_web_page_preview=True)



HelpMenu("statistics").add(
    "count", None, "A brief overview of the number of chats I am in."
).add(
    "stats", None, "A detailed overview of the number of chats I am in."
).add(
    "reserved", None, "List of all the public usernames in my possession."
).add(
    "info", "<reply> or <username/id>", "Get the user's detailed info.", "info @ForGo10God"
).info(
    "Statistics Module"
).done()
