import datetime

from pyrogram import Client, filters
from pyrogram.types import Message

from Hellbot.core import ENV, LOGS

from . import HelpMenu, custom_handler, db, hellbot, on_message


@on_message("save", allow_stan=True)
async def save_message(client: Client, message: Message):
    if len(message.command) >= 2:
        to_save = message.command[1]
        await client.send_message(
            "me",
            f"Saved on {datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}:\n\n```{to_save}```",
            disable_web_page_preview=True,
        )
    elif message.reply_to_message:
        to_save = message.reply_to_message.id
        await client.forward_messages(
            "me",
            message.chat.id,
            to_save,
        )
    await message.delete()


@custom_handler(filters.incoming & filters.private & ~filters.bot)
async def pm_logger(client: Client, message: Message):
    if message.from_user.id == 777000:
        return

    logger = await db.get_env(ENV.pm_logger)
    try:
        if logger:
            if message.chat.id != client.me.id:
                await message.forward(int(logger), True)
    except Exception as e:
        LOGS.warning(f"PM Logger Err: {e}")
