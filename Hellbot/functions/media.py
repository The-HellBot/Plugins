import os
from typing import Union

import requests
from pyrogram import Client
from pyrogram.file_id import FileId
from pyrogram.raw.functions.messages import UploadMedia
from pyrogram.raw.types import (
    DocumentAttributeFilename,
    InputDocument,
    InputMediaUploadedDocument,
)
from pyrogram.types import Animation, Audio, Document, Message, Photo, Sticker, Video

from Hellbot.core import Symbols


async def get_metedata(media: Union[Animation, Audio, Document, Photo, Sticker, Video]):
    output = "📄 MetaData:\n\n"
    if isinstance(media, Animation):
        output += f"<b>{Symbols.diamond_2} File ID:</b> <code>{media.file_id}</code>\n"
        output += f"<b>{Symbols.diamond_2} Width:</b> <code>{media.width}</code>\n"
        output += f"<b>{Symbols.diamond_2} Height:</b> <code>{media.height}</code>\n"
        output += (
            f"<b>{Symbols.diamond_2} Duration:</b> <code>{media.duration}</code>\n"
        )
        output += (
            f"<b>{Symbols.diamond_2} File Name:</b> <code>{media.file_name}</code>\n"
        )
        output += (
            f"<b>{Symbols.diamond_2} Mime Type:</b> <code>{media.mime_type}</code>\n"
        )
        output += (
            f"<b>{Symbols.diamond_2} File Size:</b> <code>{media.file_size}</code>\n"
        )
        output += f"<b>{Symbols.diamond_2} Date:</b> <code>{media.date}</code>\n"
        output += f"<b>{Symbols.diamond_2} File Type:</b> <code>Animation</code>\n"
    elif isinstance(media, Audio):
        output += f"<b>{Symbols.diamond_2} File ID:</b> <code>{media.file_id}</code>\n"
        output += (
            f"<b>{Symbols.diamond_2} Duration:</b> <code>{media.duration}</code>\n"
        )
        output += (
            f"<b>{Symbols.diamond_2} Performer:</b> <code>{media.performer}</code>\n"
        )
        output += f"<b>{Symbols.diamond_2} Title:</b> <code>{media.title}</code>\n"
        output += (
            f"<b>{Symbols.diamond_2} File Name:</b> <code>{media.file_name}</code>\n"
        )
        output += (
            f"<b>{Symbols.diamond_2} Mime Type:</b> <code>{media.mime_type}</code>\n"
        )
        output += (
            f"<b>{Symbols.diamond_2} File Size:</b> <code>{media.file_size}</code>\n"
        )
        output += f"<b>{Symbols.diamond_2} Date:</b> <code>{media.date}</code>\n"
        output += f"<b>{Symbols.diamond_2} File Type:</b> <code>Audio</code>\n"
    elif isinstance(media, Document):
        output += f"<b>{Symbols.diamond_2} File ID:</b> <code>{media.file_id}</code>\n"
        output += (
            f"<b>{Symbols.diamond_2} File Name:</b> <code>{media.file_name}</code>\n"
        )
        output += (
            f"<b>{Symbols.diamond_2} Mime Type:</b> <code>{media.mime_type}</code>\n"
        )
        output += (
            f"<b>{Symbols.diamond_2} File Size:</b> <code>{media.file_size}</code>\n"
        )
        output += f"<b>{Symbols.diamond_2} Date:</b> <code>{media.date}</code>\n"
        output += f"<b>{Symbols.diamond_2} File Type:</b> <code>Document</code>\n"
    elif isinstance(media, Photo):
        output += f"<b>{Symbols.diamond_2} File ID:</b> <code>{media.file_id}</code>\n"
        output += f"<b>{Symbols.diamond_2} Width:</b> <code>{media.width}</code>\n"
        output += f"<b>{Symbols.diamond_2} Height:</b> <code>{media.height}</code>\n"
        output += f"<b>{Symbols.diamond_2} File Name:</b> <code>photo.jpg</code>\n"
        output += f"<b>{Symbols.diamond_2} Mime Type:</b> <code>image/jpeg</code>\n"
        output += (
            f"<b>{Symbols.diamond_2} File Size:</b> <code>{media.file_size}</code>\n"
        )
        output += f"<b>{Symbols.diamond_2} Date:</b> <code>{media.date}</code>\n"
        output += f"<b>{Symbols.diamond_2} File Type:</b> <code>Photo</code>\n"
    elif isinstance(media, Sticker):
        output += f"<b>{Symbols.diamond_2} File ID:</b> <code>{media.file_id}</code>\n"
        output += f"<b>{Symbols.diamond_2} Width:</b> <code>{media.width}</code>\n"
        output += f"<b>{Symbols.diamond_2} Height:</b> <code>{media.height}</code>\n"
        output += (
            f"<b>{Symbols.diamond_2} File Name:</b> <code>{media.file_name}</code>\n"
        )
        output += (
            f"<b>{Symbols.diamond_2} Mime Type:</b> <code>{media.mime_type}</code>\n"
        )
        output += (
            f"<b>{Symbols.diamond_2} File Size:</b> <code>{media.file_size}</code>\n"
        )
        output += f"<b>{Symbols.diamond_2} Date:</b> <code>{media.date}</code>\n"
        output += f"<b>{Symbols.diamond_2} Emoji:</b> <code>{media.emoji}</code>\n"
        output += (
            f"<b>{Symbols.diamond_2} Set Name:</b> <code>{media.set_name}</code>\n"
        )
        output += f"<b>{Symbols.diamond_2} File Type:</b> <code>Sticker</code>\n"
    elif isinstance(media, Video):
        output += f"<b>{Symbols.diamond_2} File ID:</b> <code>{media.file_id}</code>\n"
        output += f"<b>{Symbols.diamond_2} Width:</b> <code>{media.width}</code>\n"
        output += f"<b>{Symbols.diamond_2} Height:</b> <code>{media.height}</code>\n"
        output += (
            f"<b>{Symbols.diamond_2} Duration:</b> <code>{media.duration}</code>\n"
        )
        output += (
            f"<b>{Symbols.diamond_2} File Name:</b> <code>{media.file_name}</code>\n"
        )
        output += (
            f"<b>{Symbols.diamond_2} Mime Type:</b> <code>{media.mime_type}</code>\n"
        )
        output += (
            f"<b>{Symbols.diamond_2} File Size:</b> <code>{media.file_size}</code>\n"
        )
        output += f"<b>{Symbols.diamond_2} Date:</b> <code>{media.date}</code>\n"
        output += f"<b>{Symbols.diamond_2} File Type:</b> <code>Video</code>\n"
    else:
        return None

    return output


def get_media_text_ocr(filename: str, api_key: str, language: str = "eng") -> dict:
    payload = {
        "isOverlayRequired": False,
        "apikey": api_key,
        "language": language,
    }

    with open(filename, "rb") as f:
        r = requests.post(
            "https://api.ocr.space/parse/image",
            files={filename: f},
            data=payload,
        )

    return r.json()


async def upload_media(client: Client, chat_id: int, file: str) -> InputDocument:
    media = await client.invoke(
        UploadMedia(
            peer=(await client.resolve_peer(chat_id)),
            media=InputMediaUploadedDocument(
                file=(await client.save_file(file)),
                mime_type=client.guess_mime_type(file) or "application/zip",
                attributes=[
                    DocumentAttributeFilename(file_name=os.path.basename(file))
                ],
                force_file=True,
            ),
        ),
    )

    return InputDocument(
        id=media.document.id,
        access_hash=media.document.access_hash,
        file_reference=media.document.file_reference,
    )


async def get_media_from_id(file_id: str) -> InputDocument:
    file = FileId.decode(file_id)

    return InputDocument(
        id=file.media_id,
        access_hash=file.access_hash,
        file_reference=file.file_reference,
    )


async def get_media_fileid(message: Message) -> str | None:
    file_id = None
    if message.photo:
        file_id = message.photo.file_id
    elif message.animation:
        file_id = message.animation.file_id
    elif message.audio:
        file_id = message.audio.file_id
    elif message.document:
        file_id = message.document.file_id
    elif message.video:
        file_id = message.video.file_id
    elif message.sticker:
        file_id = message.sticker.file_id
    elif message.video_note:
        file_id = message.video_note.file_id
    elif message.voice:
        file_id = message.voice.file_id
    return file_id
