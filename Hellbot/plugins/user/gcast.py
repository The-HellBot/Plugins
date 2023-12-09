from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from Hellbot.functions.utility import Gcast

from . import HelpMenu, handler, hellbot, on_message

gcast = Gcast()


@on_message("gcast", allow_stan=True)
async def broadcast(client: Client, message: Message):
    if len(message.command) < 2 or not message.reply_to_message:
        return await hellbot.delete(
            message,
            f"Reply to a message with {handler}gcast <all / groups / users> <copy>",
        )

    mode = message.command[1].lower()
    if mode not in ["all", "groups", "users"]:
        return await hellbot.delete(
            message,
            f"Reply to a message with {handler}gcast <all / groups / users> <copy>",
        )

    tag = True
    if len(message.command) > 2:
        is_copy = message.command[2].lower()
        tag = False if is_copy == "copy" else True

    hell = await hellbot.edit(message, "Processing...")
    msg = await gcast.start(
        message.reply_to_message, client, message.command[1].strip(), tag
    )

    if msg:
        await hell.edit(
            msg[1], parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
        )
        await hellbot.check_and_log("gcast", msg[1], msg[0])
    else:
        await hell.edit("No user or group found!")


HelpMenu("gcast").add(
    "gcast",
    "<target> <copy>",
    "Broadcast the replied message to selected target. If 'copy' is also passed the gcast will be without forward tag. Bydefault gcast is done with a forward tag.",
    "gcast groups copy",
    "Target: all, groups, users",
).info("Broadcast Module").done()
