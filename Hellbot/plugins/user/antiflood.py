import asyncio
import datetime
import time

from pyrogram import Client, filters
from pyrogram.types import ChatPermissions, Message

from Hellbot.core import Config, Symbols, db
from Hellbot.functions.utility import Flood

from . import HelpMenu, custom_handler, group_only, hellbot, on_message


@on_message("setflood", chat_type=group_only, admin_only=True, allow_stan=True)
async def setflood(client: Client, message: Message):
    count = 5
    mtime = 0
    mode = "mute"

    try:
        time_data = "N/A"
        if len(message.command) == 2:
            count = int(message.command[1])
        elif len(message.command) == 3:
            count = int(message.command[1])
            mode = message.command[2]
        elif len(message.command) >= 4:
            count = int(message.command[1])
            mode = message.command[2]
            time_data = message.command[3]
            if time_data.endswith(("d", "day", "days")):
                mtime = int(time_data.split("d")[0].strip()) * 24 * 60 * 60
            elif time_data.endswith(("h", "hrs", "hour", "hours")):
                mtime = int(time_data.split("h")[0].strip()) * 60 * 60
            elif time_data.endswith(("m", "mins", "minute", "minutes")):
                mtime = int(time_data.split("m")[0].strip()) * 60
            else:
                return await hellbot.error(
                    message,
                    "Please pass time in correct format!\n\nExample: 12d or 12h or 12m",
                )
    except Exception as e:
        return await hellbot.error(message, str(e))

    if mode.lower() not in ["mute", "kick", "ban"]:
        return await hellbot.error(
            message, "**Invalid mode! Choose one: **\n`mute`, `kick`, `ban`"
        )

    settings = {
        "mode": mode,
        "limit": count,
        "time": mtime,
    }

    await db.set_flood((client.me.id, message.chat.id), settings)
    Flood.updateSettings(client.me.id, message.chat.id, settings)

    if count == 0:
        return await hellbot.delete(message, "Antiflood disabled!")

    await hellbot.delete(
        message,
        f"**Antiflood enabled!**\n\n**{Symbols.triangle_right} Mode:** `{mode}`\n**{Symbols.triangle_right} Limit:** `{count}`\n**{Symbols.triangle_right} Time:** `{time_data}`",
        20,
    )


@custom_handler(
    filters.all
    & filters.group
    & filters.incoming
    & ~filters.bot
    & ~Config.AUTH_USERS
    & ~filters.me
    & ~filters.service
)
async def antiflood(client: Client, message: Message):
    mode, mtime, limit = Flood.getSettings(client.me.id, message.chat.id)

    if limit == 0:
        return
    if not Flood.check_client_chat(client.me.id, message.chat.id):
        return

    last_user, count = Flood.getLastUser(client.me.id, message.chat.id)

    if last_user == message.from_user.id:
        if (count + 1) >= limit:
            template = (
                "**🤫 𝖠𝗇𝗍𝗂𝖥𝗅𝗈𝗈𝖽 {mode}!!** \n\n"
                "**{symbol} 𝖴𝗌𝖾𝗋:** `{mention}`\n"
                "**{symbol} 𝖳𝗂𝗅𝗅 𝖣𝖺𝗍𝖾:** `🗓️ {till_date}`\n"
            )
            hell = await message.reply_text("Flood Detected!")

            if mode == "mute":
                permission = ChatPermissions(can_send_messages=False)
                until_date = datetime.datetime.fromtimestamp(time.time() + mtime)
                try:
                    await client.restrict_chat_member(
                        message.chat.id,
                        message.from_user.id,
                        permission,
                        until_date,
                    )
                except Exception as e:
                    return await hellbot.error(
                        hell, f"__Error in Antiflood while trying to mute!__\n{str(e)}"
                    )

                Flood.updateFlood(
                    client.me.id, message.chat.id, message.from_user.id, 0
                )
                till_date = "Forever" if mtime == 0 else until_date.ctime()

                return await hell.edit(
                    template.format(
                        mode=mode.title(),
                        symbol=Symbols.triangle_right,
                        mention=message.from_user.mention,
                        till_date=till_date,
                    )
                )

            elif mode == "kick":
                try:
                    await client.ban_chat_member(message.chat.id, message.from_user.id)
                except Exception as e:
                    return await hellbot.error(
                        hell, f"__Error in Antiflood while trying to kick!__\n{str(e)}"
                    )

                await hell.edit(
                    template.format(
                        mode=mode.title(),
                        symbol=Symbols.triangle_right,
                        mention=message.from_user.mention,
                        till_date="Kicked Users can join back after 5 seconds!",
                    )
                )
                Flood.updateFlood(
                    client.me.id, message.chat.id, message.from_user.id, 0
                )
                await asyncio.sleep(5)
                await client.unban_chat_member(message.chat.id, message.from_user.id)
                return

            elif mode == "ban":
                until_date = datetime.datetime.fromtimestamp(time.time() + mtime)
                try:
                    await client.ban_chat_member(
                        message.chat.id,
                        message.from_user.id,
                        until_date,
                    )
                except Exception as e:
                    return await hellbot.error(
                        hell, f"__Error in Antiflood while trying to ban!__\n{str(e)}"
                    )

                Flood.updateFlood(
                    client.me.id, message.chat.id, message.from_user.id, 0
                )
                till_date = "Forever" if mtime == 0 else until_date.ctime()

                return await hell.edit(
                    template.format(
                        mode=mode.title(),
                        symbol=Symbols.triangle_right,
                        mention=message.from_user.mention,
                        till_date=till_date,
                    )
                )
            else:
                return
        else:
            count += 1
            Flood.updateFlood(
                client.me.id, message.chat.id, message.from_user.id, count
            )
            return
    else:
        Flood.updateFlood(client.me.id, message.chat.id, message.from_user.id, 1)


HelpMenu("antiflood").add(
    "setflood",
    "<limit> <mode> <time>",
    "Set antiflood in the chat! All arguments are optional, bydefault limit is 5 and mode is permanent mute.",
    "setflood 10 ban 1d",
    "Mode can be mute, kick or ban. Time can be xd (days), xh (hours) or xm (minutes) where x is number.",
).add(
    "setflood 0",
    None,
    "Disable antiflood in the chat!",
    "setflood 0",
).info(
    "Control Flood in the chat!"
).done()
