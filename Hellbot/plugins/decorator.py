from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from Hellbot.core import Config, hellbot
from Hellbot.functions.admins import is_user_admin


def on_message(
    command: str | list[str],
    group: int = 0,
    chat_type: list[ChatType] = None,
    admin_only: bool = False,
    allow_sudo: bool = False,
):
    if allow_sudo:
        _filter = (
            filters.command(command, Config.HANDLERS)
            & (filters.me | Config.SUDO_USERS)
            & ~filters.forwarded
            & ~filters.via_bot
        )
    else:
        _filter = (
            filters.command(command, Config.HANDLERS)
            & filters.me
            & ~filters.forwarded
            & ~filters.via_bot
        )

    def decorator(func):
        async def wrapper(client: Client, message: Message):
            if admin_only and not await is_user_admin(message, message.from_user.id):
                return await hellbot.edit(message, "𝖨 𝖺𝗆 𝗇𝗈𝗍 𝖺𝗇 𝖺𝖽𝗆𝗂𝗇 𝗁𝖾𝗋𝖾!")

            if chat_type and message.chat.type not in chat_type:
                return await hellbot.edit(message, f"𝖴𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗂𝗇 {chat_type.name} 𝗈𝗇𝗅𝗒!")

            await func(client, message)

        for user in hellbot.users:
            user.add_handler(MessageHandler(wrapper, _filter), group)

        return wrapper

    return decorator
