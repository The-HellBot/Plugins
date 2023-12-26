from typing import Tuple

from emoji import EMOJI_DATA
from pyrogram import Client
from pyrogram.raw.functions.messages import GetStickerSet
from pyrogram.raw.functions.stickers import AddStickerToSet, CreateStickerSet, RemoveStickerFromSet
from pyrogram.raw import base, types
from pyrogram.types import Message

from .media import get_media_from_id, upload_media


def is_emoji(text: str) -> bool:
    return any(c in EMOJI_DATA for c in text)


def get_emoji_and_id(message: Message) -> Tuple[int, str]:
    pack_id = None
    pack_emoji = None

    for command in message.command:
        if command.isdigit():
            pack_id = int(command)
        elif is_emoji(command):
            pack_emoji = command

    if pack_id is None:
        pack_id = 1

    if pack_emoji is None:
        sticker = message.reply_to_message.sticker
        try:
            pack_emoji = sticker.emoji if sticker and sticker.emoji else "🍀"
        except:
            pack_emoji = "🍀"

    return pack_id, pack_emoji


def check_sticker_data(replied: Message) -> Tuple[str | None, bool, bool, bool, int]:
    pack_type = None
    is_animated = False
    is_video = False
    is_static = False
    pack_limit = 50

    if replied.sticker:
        if replied.sticker.is_animated:
            pack_type, is_animated = "animated", True
        elif replied.sticker.is_video:
            pack_type, is_video = "video", True
        else:
            pack_type, is_static, pack_limit = "static", True, 120

    elif replied.photo:
        pack_type, is_static, pack_limit = "static", True, 120

    elif replied.video or replied.animation:
        pack_type, is_video = "video", True

    elif replied.document:
        mime_type = replied.document.mime_type.lower()
        if mime_type.startswith("video/"):
            pack_type, is_video = "video", True
        elif mime_type.startswith("image/"):
            pack_type, is_static, pack_limit = "static", True, 120
        elif mime_type in ["application/x-tgsticker", "application/x-bad-tgsticker"]:
            pack_type, is_animated = "animated", True

    return pack_type, is_animated, is_video, is_static, pack_limit


async def create_sticker(
    client: Client,
    chat_id: int,
    file: str,
    emoji: str,
) -> types.InputStickerSetItem:
    sticker = await upload_media(client, chat_id, file)

    return types.InputStickerSetItem(
        document=sticker,
        emoji=emoji,
    )


async def remove_sticker(client: Client, stickerid: str) -> base.messages.StickerSet:
    sticker = await get_media_from_id(stickerid)
    return await client.invoke(RemoveStickerFromSet(sticker=sticker))


async def get_sticker_set(client: Client, name: str) -> base.messages.StickerSet | None:
    try:
        return await client.invoke(
            GetStickerSet(
                stickerset=types.InputStickerSetShortName(short_name=name),
                hash=0,
            )
        )
    except:
        return None


async def add_sticker(
    client: Client,
    stickerset: base.messages.StickerSet,
    sticker: base.InputStickerSetItem,
) -> base.messages.StickerSet:
    return await client.invoke(
        AddStickerToSet(
            stickerset=types.InputStickerSetShortName(short_name=stickerset.set.short_name),
            sticker=sticker,
        )
    )


async def new_sticker_set(
    client: Client,
    user_id: int,
    title: str,
    short_name: str,
    stickers: list[base.InputStickerSetItem],
    animated: bool,
    video: bool,
) -> base.messages.StickerSet:
    return await client.invoke(
        CreateStickerSet(
            user_id=(await client.resolve_peer(user_id)),
            title=title,
            short_name=short_name,
            stickers=stickers,
            animated=animated,
            videos=video,
        )
    )
