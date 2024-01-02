import os

from pyrogram import Client
from pyrogram.errors import PeerIdInvalid, UserIsBlocked
from pyrogram.raw.types import InputDocument, InputStickerSetItem
from pyrogram.types import Message

from Hellbot.core import ENV
from Hellbot.functions.convert import image_to_sticker, video_to_sticker
from Hellbot.functions.sticker import (
    add_sticker,
    check_sticker_data,
    create_sticker,
    get_emoji_and_id,
    get_sticker_set,
    new_sticker_set,
    remove_sticker,
)

from . import Config, HelpMenu, Symbols, db, hellbot, on_message


@on_message("kang", allow_stan=True)
async def kangSticker(client: Client, message: Message):
    if not message.reply_to_message:
        return await hellbot.delete(message, "Reply to a sticker to kang it.")

    hell = await hellbot.edit(message, "__Kanging sticker...__")

    pack_id, pack_emoji = get_emoji_and_id(message)
    pack_type, is_animated, is_video, is_static, pack_limit = check_sticker_data(
        message.reply_to_message
    )

    if pack_type is None:
        return await hellbot.delete(hell, "Unsupported media type.")

    nickname = f"@{client.me.username}" if client.me.username else client.me.first_name
    pack_name = (
        await db.get_env(ENV.sticker_packname)
        or f"{nickname}'s Vol.{pack_id} ({pack_type.title()})"
    )
    pack_url_suffix = (
        f"HB{client.me.id}_vol{pack_id}_{pack_type}_by_{hellbot.bot.me.username}"
    )

    if message.reply_to_message.sticker:
        if is_static:
            file = await message.reply_to_message.download(Config.TEMP_DIR)
            status, path = await image_to_sticker(file)
            if not status:
                return await hellbot.error(hell, path)
        else:
            path = await message.reply_to_message.download(Config.TEMP_DIR)
    else:
        if is_video:
            await hell.edit("Converting to video sticker...")
            path, status = await video_to_sticker(message.reply_to_message)
            if not status:
                return await hellbot.error(hell, path)
        elif is_animated:
            await hell.edit("Converting to animated sticker...")
            path = await message.reply_to_message.download(Config.TEMP_DIR)
        else:
            await hell.edit("Converting to sticker...")
            file = await message.reply_to_message.download(Config.TEMP_DIR)
            status, path = await image_to_sticker(file)
            if not status:
                return await hellbot.error(hell, path)

    sticker = await create_sticker(hellbot.bot, Config.LOGGER_ID, path, pack_emoji)
    os.remove(path)

    try:
        while True:
            stickerset = await get_sticker_set(hellbot.bot, pack_url_suffix)
            if stickerset:
                if stickerset.set.count == pack_limit:
                    pack_id += 1
                    pack_name = (
                        await db.get_env(ENV.sticker_packname)
                        or f"{nickname}'s Vol.{pack_id} ({pack_type.title()})"
                    )
                    pack_url_suffix = f"HB{client.me.id}_vol{pack_id}_{pack_type}_by_{hellbot.bot.me.username}"
                    continue
                else:
                    await add_sticker(hellbot.bot, stickerset, sticker)
            else:
                await new_sticker_set(
                    hellbot.bot,
                    client.me.id,
                    pack_name,
                    pack_url_suffix,
                    [sticker],
                    is_animated,
                    is_video,
                )
            break
        return await hell.edit(
            f"**{pack_emoji} 𝖲𝗍𝗂𝖼𝗄𝖾𝗋 𝗄𝖺𝗇𝗀𝖾𝖽 𝗍𝗈 [this pack](t.me/addstickers/{pack_url_suffix})**",
            disable_web_page_preview=True,
        )
    except (PeerIdInvalid, UserIsBlocked):
        return await hellbot.delete(
            hell, f"Start @{hellbot.bot.me.username} first and try to kang again.", 20
        )
    except Exception as e:
        return await hellbot.error(hell, str(e))


@on_message("packkang", allow_stan=True)
async def packKang(client: Client, message: Message):
    if not message.reply_to_message:
        return await hellbot.delete(message, "Reply to a sticker to kang whole pack!")

    hell = await hellbot.edit(message, "__Kanging sticker pack...__")

    pack_id = 1
    nickname = f"@{client.me.username}" if client.me.username else client.me.first_name
    packname = await hellbot.input(message) or f"{nickname}'s Pack (Vol.{pack_id})"
    pack_url_suffix = f"HB{client.me.id}_pkvol{pack_id}_by_{hellbot.bot.me.username}"

    if not message.reply_to_message.sticker:
        return await hellbot.delete(hell, "Reply to a sticker to kang whole pack!")

    is_animated = message.reply_to_message.sticker.is_animated
    is_video = message.reply_to_message.sticker.is_video

    stickers = []
    replied_setname = message.reply_to_message.sticker.set_name
    replied_set = await get_sticker_set(hellbot.bot, replied_setname)
    if not replied_set:
        return await hellbot.delete(hell, "Reply to a sticker to kang whole pack!")

    for sticker in replied_set.documents:
        document = InputDocument(
            id=sticker.id,
            access_hash=sticker.access_hash,
            file_reference=sticker.file_reference,
        )
        stickers.append(InputStickerSetItem(document=document, emoji="🍀"))
    try:
        while True:
            stickerset = await get_sticker_set(hellbot.bot, pack_url_suffix)
            if stickerset:
                pack_id += 1
                pack_url_suffix = (
                    f"HB{client.me.id}_pkvol{pack_id}_by_{hellbot.bot.me.username}"
                )
                packname = (
                    await hellbot.input(message) or f"{nickname}'s Pack (Vol.{pack_id})"
                )
                continue
            else:
                await new_sticker_set(
                    hellbot.bot,
                    client.me.id,
                    packname,
                    pack_url_suffix,
                    stickers,
                    is_animated,
                    is_video,
                )
                break
        return await hell.edit(
            f"**🍀 𝖲𝗍𝗂𝖼𝗄𝖾𝗋 𝖯𝖺𝖼𝗄 𝗄𝖺𝗇𝗀𝖾𝖽 𝗍𝗈 [this pack](t.me/addstickers/{pack_url_suffix})**",
            disable_web_page_preview=True,
        )
    except (PeerIdInvalid, UserIsBlocked):
        return await hellbot.delete(
            hell, f"Start @{hellbot.bot.me.username} first and try to kang again.", 20
        )
    except Exception as e:
        return await hellbot.error(hell, str(e))


@on_message("stickerinfo", allow_stan=True)
async def stickerInfo(_, message: Message):
    if not message.reply_to_message or not message.reply_to_message.sticker:
        return await hellbot.delete(message, "Reply to a sticker to get their info.")

    hell = await hellbot.edit(message, "__Fetching sticker info ...__")

    sticker = message.reply_to_message.sticker

    sticker_set = await get_sticker_set(hellbot.bot, sticker.set_name)
    if not sticker_set:
        return await hellbot.delete(hell, "This sticker is not part of a pack.")

    pack_emoji = []
    for emojis in sticker_set.packs:
        if emojis.emoticon not in pack_emoji:
            pack_emoji.append(emojis.emoticon)

    outStr = (
        f"**🍀 𝖲𝗍𝗂𝖼𝗄𝖾𝗋 𝖯𝖺𝖼𝗄 𝖨𝗇𝖿𝗈:**\n\n"
        f"**{Symbols.diamond_2} 𝖲𝗍𝗂𝖼𝗄𝖾𝗋 𝖨𝖣:** `{sticker.file_id}`\n"
        f"**{Symbols.diamond_2} Pack Name:** `{sticker_set.set.title}`\n"
        f"**{Symbols.diamond_2} Pack Short Name:** `{sticker_set.set.short_name}`\n"
        f"**{Symbols.diamond_2} 𝖮𝖿𝖿𝗂𝖼𝗂𝖺𝗅:** {sticker_set.set.official}\n"
        f"**{Symbols.diamond_2} 𝖤𝗆𝗈𝗃𝗂:** `{', '.join(pack_emoji)}`\n"
        f"**{Symbols.diamond_2} 𝖣𝖺𝗍𝖾:** `{sticker_set.set.installed_date}`\n"
        f"**{Symbols.diamond_2} 𝖲𝗍𝗂𝖼𝗄𝖾𝗋 𝖲𝗂𝗓𝖾:** `{sticker_set.set.count}`\n"
    )

    await hell.edit(outStr, disable_web_page_preview=True)


@on_message("rmsticker", allow_stan=True)
async def removeSticker(_, message: Message):
    if not message.reply_to_message or not message.reply_to_message.sticker:
        return await hellbot.delete(
            message, "Reply to a sticker to remove it from the pack."
        )

    hell = await hellbot.edit(message, "__Removing sticker from pack...__")

    sticker = message.reply_to_message.sticker
    sticker_set = await get_sticker_set(hellbot.bot, sticker.set_name)
    if not sticker_set:
        return await hellbot.delete(hell, "This sticker is not part of a pack.")

    try:
        await remove_sticker(hellbot.bot, sticker.file_id)
        await hellbot.delete(
            hell, f"**𝖣𝖾𝗅𝖾𝗍𝖾𝖽 𝗍𝗁𝖾 𝗌𝗍𝗂𝖼𝗄𝖾𝗋 𝖿𝗋𝗈𝗆 𝗉𝖺𝖼𝗄:** {sticker_set.set.title}",
        )
    except Exception as e:
        await hellbot.error(hell, str(e))


HelpMenu("sticker").add(
    "kang",
    "<reply> <packid (optional)> <emoji (optional)>",
    "Add the replied image/gif/video/sticker into your own sticker pack.",
    "kang 2 👀",
    "If no emoji is given by default 🍀 will be used,.,"
).add(
    "packkang",
    "<reply> <packname>",
    "Add all the stickers in the replied pack into your own sticker pack.",
    "packkang packname",
).add(
    "stickerinfo", "<reply>", "Get info about the replied sticker.", "stickerinfo"
).add(
    "rmsticker", "<reply>", "Remove the replied sticker from the pack.", "rmsticker"
).info(
    "Sticker Manager"
).done()
