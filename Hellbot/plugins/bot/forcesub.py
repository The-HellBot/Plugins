from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired, UserNotParticipant
from pyrogram.types import (
    CallbackQuery,
    ChatPermissions,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from Hellbot.core import LOGS
from Hellbot.functions.admins import is_user_admin

from ..btnsG import gen_inline_keyboard
from . import BotHelp, Config, Symbols, db, hellbot


@hellbot.bot.on_message(filters.command("forcesub") & Config.AUTH_USERS & filters.group)
async def force_sub(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Give a channel username with command!")

    try:
        is_admin = await is_user_admin(message.chat, client.me.id)
        if not is_admin:
            return await message.reply_text(f"To use forcesub i must be an admin in {must_join}!")
    except UserNotParticipant:
        return await message.reply_text(f"To use forcesub i must be an admin in {must_join}!")

    must_join = message.command[1]
    try:
        chat = await client.get_chat(must_join)
    except Exception as e:
        return await message.reply_text(f"**Error:**\n`{e}`")

    if not await is_user_admin(chat, client.me.id):
        return await message.reply_text("Make me admin in that channel first!")

    await db.add_forcesub(message.chat.id, chat.id)
    await message.reply_text(
        f"**📌 𝖢𝗁𝖺𝗍 𝖥𝗈𝗋𝖼𝖾𝗌𝗎𝖻 𝖤𝗇𝖺𝖻𝗅𝖾𝖽!** \n\n"
        f"__Users must join__ {chat.title} (`{chat.id}`) __to chat here!__"
    )

    if message.chat.id not in Config.FORCESUBS:
        Config.FORCESUBS.add(message.chat.id)


@hellbot.bot.on_message(filters.command("unforcesub") & Config.AUTH_USERS)
async def unforce_sub(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "Give a channel username with command or give 'all' to remove all forcesubs from this chat!"
        )

    if not await is_user_admin(message.chat, client.me.id):
        return await message.reply_text("To use forcesub i must be an admin!")

    if "all" == message.command[1].lower():
        await db.rm_all_forcesub(message.chat.id)
        Config.FORCESUBS.remove(message.chat.id)
        return await message.reply_text(f"**📌 Forcesub disabled!**")

    try:
        if await db.is_forcesub(message.chat.id, int(message.command[1])):
            remaining = await db.rm_forcesub(message.chat.id, int(message.command[1]))
            if remaining:
                return await message.reply_text(
                    f"**📌 Removed Forcesub `{message.command[1]}`!**\n\n**Remaining Forcesub(s) in this chat:** `{remaining}`"
                )
            else:
                Config.FORCESUBS.remove(message.chat.id)
                return await message.reply_text(
                    f"**📌 Removed Forcesub `{message.command[1]}`!**"
                )
        else:
            return await message.reply_text(f"**📌 This chat is not forcesub enabled!**")
    except Exception as e:
        return await message.reply_text(f"**Error:**\n`{e}`")


@hellbot.bot.on_message(filters.command("listforcesub") & Config.AUTH_USERS)
async def list_force_subs(client: Client, message: Message):
    if not await is_user_admin(message.chat, client.me.id):
        return await message.reply_text("To use forcesub i must be an admin!")

    all_forcesubs = Config.FORCESUBS

    text = ""
    if len(all_forcesubs) > 0:
        for forcesub in all_forcesubs:
            try:
                chat = await client.get_chat(forcesub["chat"])
                text += f"**📌 {chat.title}** (`{chat.id}`)\n"
            except:
                text += f"**📌 {forcesub['chat']}** - `Invalid Chat!`\n"
    else:
        text = "**📌 No Forcesub Enabled in Bot!**"

    await message.reply_text(text)


@hellbot.bot.on_message(filters.command("getforcesub") & Config.AUTH_USERS)
async def getforcesub(client: Client, message: Message):
    if len(message.command) < 2:
        chat = message.chat
    else:
        try:
            chat = await client.get_chat(message.command[1])
        except:
            return await message.reply_text(f"**Invalid Channel Username/ID!**")

    mustjoins = await db.get_forcesub(chat.id)
    if mustjoins:
        text = f"**This chat has {len(mustjoins['must_join'])} forcesub(s):**\n"
        for must_join in mustjoins["must_join"]:
            try:
                chat = await client.get_chat(must_join)
                text += f"**📌 {chat.title}** (`{chat.id}`)\n"
            except:
                text += f"**📌 {must_join}** - `Invalid Chat!`\n"
    else:
        text = "**📌 No Forcesub Enabled in This Chat!**"

    await message.reply_text(text)


@hellbot.bot.on_message(
    filters.group
    & filters.incoming
    & filters.new_chat_members
    & ~filters.bot
    & ~filters.service
    & ~Config.AUTH_USERS
    & ~filters.me
)
async def handle_force_sub(client: Client, message: Message):
    if message.chat.id not in Config.FORCESUBS:
        return

    if not is_user_admin(message.chat, client.me.id):
        return

    btns_list = []
    mustjoins = await db.get_forcesub(message.chat.id)

    for i, must_join in enumerate(mustjoins["must_join"]):
        try:
            await client.get_chat_member(must_join, message.from_user.id)
        except UserNotParticipant:
            invite_link = await client.export_chat_invite_link(must_join)
            btns_list.append((f"Join {i}", invite_link, "url"))
            continue
        except ChatAdminRequired:
            continue
        except Exception as e:
            LOGS.warning(e)
            continue

    if len(btns_list) == 0:
        return

    join_btns = gen_inline_keyboard(btns_list, 2)
    join_btns.append(
        [
            InlineKeyboardButton("Unmute 🗣️", f"forcesub:unmute:{message.from_user.id}:{message.chat.id}")
        ]
    )
    await message.reply_text(
        f"**👋 Welcome to {message.chat.title}!**\n\n"
        f"To be able to chat here, you must follow the instructions below:\n"
        f"  {Symbols.anchor} __Click the buttons below to join our important channels.__"
        f"  {Symbols.anchor} __After joining all channels, press the unmute button below.__"
        f"  {Symbols.anchor} __Then you can chat here.__",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(join_btns),
    )


@hellbot.bot.on_callback_query(filters.regex(r"forcesub"))
async def forcesub_cb(client: Client, cb: CallbackQuery):
    data = cb.data.split(":")
    if data[1] == "unmute":
        try:
            if not int(data[3]) == cb.message.chat.id:
                return await cb.answer(
                    "**This is not for this chat!**", show_alert=True
                )

            must_join = await db.get_forcesub(cb.message.chat.id)
            for chat in must_join["must_join"]:
                try:
                    await client.get_chat_member(int(chat), cb.from_user.id)
                except UserNotParticipant:
                    return await cb.answer(
                        "**You must join all channels first!**", show_alert=True
                    )
                except ChatAdminRequired:
                    return await cb.answer(
                        "I'm not admin in some of the channels! Ask owner to make me admin.",
                        show_alert=True,
                    )
                except Exception as e:
                    return await cb.answer(f"**Error:**\n`{e}`")

            permissions = ChatPermissions(can_send_messages=True)
            await cb.message.chat.restrict_member(int(data[2]), permissions)
        except Exception as e:
            return await cb.answer(f"**Error:**\n`{e}`")

        await cb.answer("**📌 Unmuted!**", show_alert=True)
        return await cb.message.delete()


BotHelp("ForceSub").add(
    "forcesub",
    "This command is used to force users to join some channels to chat in group.",
).add(
    "unforcesub", "This command is used to remove channels from forcesub in group."
).add(
    "listforcesub", "This command is used to list all forcesub in bot."
).add(
    "getforcesub", "This command is used to get forcesub in group."
).info(
    "ForceSub 🚀"
).done()
