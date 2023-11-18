from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message

from Hellbot.core import hellbot

from . import HelpMenu, on_message, group_n_channel


@on_message(
    "setgpic",
    chat_type=group_n_channel,
    admin_only=True,
    allow_stan=True,
)
async def setgpic(_, message: Message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await hellbot.delete(
            message, "𝖱𝖾𝗉𝗅𝗒 𝗍𝗈 𝖺 𝗉𝗁𝗈𝗍𝗈 𝗍𝗈 𝗌𝖾𝗍 𝖺𝗌 𝗀𝗋𝗈𝗎𝗉 𝗉𝗋𝗈𝖿𝗂𝗅𝖾 𝗉𝗂𝖼𝗍𝗎𝗋𝖾."
        )

    status = await message.chat.set_photo(photo=message.reply_to_message.photo.file_id)
    if not status:
        return await hellbot.delete(message, "𝖲𝗈𝗋𝗋𝗒, 𝗌𝗈𝗆𝖾𝗍𝗁𝗂𝗇𝗀 𝗐𝖾𝗇𝗍 𝗐𝗋𝗈𝗇𝗀.")

    await hellbot.delete(message, "𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝗌𝖾𝗍 𝗀𝗋𝗈𝗎𝗉 𝗉𝗋𝗈𝖿𝗂𝗅𝖾 𝗉𝗂𝖼𝗍𝗎𝗋𝖾.")
    await hellbot.check_and_log(
        "setgpic",
        f"**Group Profile Picture**\n\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`\n**Admin:** `{message.from_user.mention}`",
    )


@on_message(
    "setgtitle",
    chat_type=group_n_channel,
    admin_only=True,
    allow_stan=True,
)
async def setgtitle(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(
            message, "𝖨 𝗇𝖾𝖾𝖽 𝗌𝗈𝗆𝖾𝗍𝗁𝗂𝗇𝗀 𝗍𝗈 𝗌𝖾𝗍 𝗍𝗁𝗂𝗌 𝗀𝗋𝗈𝗎𝗉 𝗍𝗂𝗍𝗅𝖾."
        )

    prev_title = message.chat.title
    new_title = await hellbot.input(message)
    status = await message.chat.set_title(new_title)
    if not status:
        return await hellbot.delete(message, "𝖲𝗈𝗋𝗋𝗒, 𝗌𝗈𝗆𝖾𝗍𝗁𝗂𝗇𝗀 𝗐𝖾𝗇𝗍 𝗐𝗋𝗈𝗇𝗀.")

    await hellbot.delete(message, "𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝗌𝖾𝗍 𝗀𝗋𝗈𝗎𝗉 𝗍𝗂𝗍𝗅𝖾.")
    await hellbot.check_and_log(
        "setgtitle",
        f"**Group Title**\n\n**Group:** `{prev_title}`\n**Group ID:** `{message.chat.id}`\n**Admin:** `{message.from_user.mention}`",
    )


@on_message(
    "setgabout",
    chat_type=group_n_channel,
    admin_only=True,
    allow_stan=True,
)
async def setgabout(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(
            message, "𝖨 𝗇𝖾𝖾𝖽 𝗌𝗈𝗆𝖾𝗍𝗁𝗂𝗇𝗀 𝗍𝗈 𝗌𝖾𝗍 𝗍𝗁𝗂𝗌 𝗀𝗋𝗈𝗎𝗉 𝖺𝖻𝗈𝗎𝗍."
        )

    new_about = await hellbot.input(message)
    status = await message.chat.set_description(new_about)
    if not status:
        return await hellbot.delete(message, "𝖲𝗈𝗋𝗋𝗒, 𝗌𝗈𝗆𝖾𝗍𝗁𝗂𝗇𝗀 𝗐𝖾𝗇𝗍 𝗐𝗋𝗈𝗇𝗀.")

    await hellbot.delete(message, "𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝗌𝖾𝗍 𝗀𝗋𝗈𝗎𝗉 𝖺𝖻𝗈𝗎𝗍.")
    await hellbot.check_and_log(
        "setgabout",
        f"**Group About**\n\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`\n**Admin:** `{message.from_user.mention}`",
    )


@on_message(
    "setgusername",
    chat_type=group_n_channel,
    admin_only=True,
    allow_stan=True,
)
async def setgusername(client: Client, message: Message):
    user_status = (await message.chat.get_member(message.from_user.id)).status
    if user_status != ChatMemberStatus.OWNER:
        return await hellbot.delete(message, "𝖨 𝖺𝗆 𝗇𝗈𝗍 𝗍𝗁𝖾 𝗈𝗐𝗇𝖾𝗋 𝗈𝖿 𝗍𝗁𝗂𝗌 𝗀𝗋𝗈𝗎𝗉.")

    if len(message.command) < 2:
        return await hellbot.delete(
            message, "𝖨 𝗇𝖾𝖾𝖽 𝗌𝗈𝗆𝖾𝗍𝗁𝗂𝗇𝗀 𝗍𝗈 𝗌𝖾𝗍 𝗍𝗁𝗂𝗌 𝗀𝗋𝗈𝗎𝗉'𝗌 𝗎𝗌𝖾𝗋𝗇𝖺𝗆𝖾."
        )

    new_username = await hellbot.input(message)
    status = await client.set_chat_username(message.chat.id, new_username)
    if not status:
        return await hellbot.delete(message, "𝖲𝗈𝗋𝗋𝗒, 𝗌𝗈𝗆𝖾𝗍𝗁𝗂𝗇𝗀 𝗐𝖾𝗇𝗍 𝗐𝗋𝗈𝗇𝗀.")

    await hellbot.delete(message, "𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝗌𝖾𝗍 𝗀𝗋𝗈𝗎𝗉 𝗎𝗌𝖾𝗋𝗇𝖺𝗆𝖾.")
    await hellbot.check_and_log(
        "setgusername",
        f"**Group Username**\n\n**Group:** `{message.chat.title}`\n**Group ID:** `{message.chat.id}`\n**Admin:** `{message.from_user.mention}`",
    )


@on_message(
    "getglink",
    chat_type=group_n_channel,
    admin_only=True,
    allow_stan=True,
)
async def getglink(_, message: Message):
    link = await message.chat.export_invite_link()
    await hellbot.delete(message, f"**𝖦𝗋𝗈𝗎𝗉 𝗅𝗂𝗇𝗄:** `{link}`")


HelpMenu("groups").add(
    "setgpic", "<reply to photo>", "Set the group profile picture.", "setgpic"
).add("setgtitle", "<title>", "Set the group title.", "setgtitle chat group").add(
    "setgabout",
    "<text>",
    "Set the group description/about",
    "setgabout some group description",
).add(
    "setgusername",
    "<username>",
    "Set the group username.",
    "setgusername HellBot_Chats",
    "Only group owners can use this command. Give username without '@'.",
).add(
    "getglink", None, "Get the group invite link.", "getglink"
).info(
    "Group Menu"
).done()
