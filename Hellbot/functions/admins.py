from pyrogram.enums import ChatMembersFilter, ChatMemberStatus, ChatType
from pyrogram.types import Chat

from Hellbot.core import hellbot


async def get_admins(chat_id: int) -> list:
    admins = []
    async for x in hellbot.bot.get_chat_members(
        chat_id, filter=ChatMembersFilter.ADMINISTRATORS
    ):
        admins.append(x.user.id)
    return admins


async def is_user_admin(chat: Chat, user_id: int) -> bool:
    if chat.type in [ChatType.PRIVATE, ChatType.BOT]:
        return True

    status = (await chat.get_member(user_id)).status
    if status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
        return True

    return False
