from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from Hellbot.core import Config, hellbot
from Hellbot.functions.admins import is_user_admin


def on_message(
    command: list = None,
    group: int = 0,
    chat_type: ChatType = None,
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
            if admin_only and not await is_user_admin(message, hellbot.me.id):
                await hellbot.edit_or_reply(message, "I am not admin here!")
                return

            if chat_type and message.chat.type != chat_type:
                await hellbot.edit_or_reply(
                    message, f"Use this command in {chat_type.name} only!"
                )
                return

            await func(client, message)

        for user in hellbot.users:
            user.add_handler(MessageHandler(wrapper, _filter), group)

        return wrapper

    return decorator
