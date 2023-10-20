from pyrogram.types import Message

from Hellbot.core import Config


async def edit_or_reply(message: Message, text: str) -> Message:
    if message.from_user:
        if message.from_user.id in Config.SUDO_USERS:
            if message.reply_to_message:
                return await message.reply_to_message.reply_text(text)
            return await message.reply_text(text)
    return await message.edit_text(text)
