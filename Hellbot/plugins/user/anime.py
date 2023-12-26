import os

from pyrogram.errors import ChatSendMediaForbidden
from pyrogram.types import Message

from Hellbot.core import hellbot
from Hellbot.functions.scraping import (
    get_airing_info,
    get_anilist_user_info,
    get_anime_info,
    get_character_info,
    get_filler_info,
    get_manga_info,
    get_watch_order,
)

from . import HelpMenu, on_message


@on_message("anime", allow_stan=True)
async def anime(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(message, "Give me an anime name to search!")

    query = await hellbot.input(message)
    hell = await hellbot.edit(message, "Searching ...")
    caption, photo = await get_anime_info(query)

    try:
        await message.reply_photo(photo, caption=caption)
        await hell.delete()
    except ChatSendMediaForbidden:
        await hell.edit(caption, disable_web_page_preview=True)

    if os.path.exists(photo):
        os.remove(photo)


@on_message("manga", allow_stan=True)
async def manga(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(message, "Give me a manga name to search!")

    query = await hellbot.input(message)
    hell = await hellbot.edit(message, "Searching ...")
    caption, photo = await get_manga_info(query)

    try:
        await message.reply_photo(photo, caption=caption)
        await hell.delete()
    except ChatSendMediaForbidden:
        await hell.edit(caption, disable_web_page_preview=True)

    if os.path.exists(photo):
        os.remove(photo)


@on_message("character", allow_stan=True)
async def character(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(message, "Give me a character name to search!")

    query = await hellbot.input(message)
    hell = await hellbot.edit(message, "Searching ...")
    caption, photo = await get_character_info(query)

    try:
        await message.reply_photo(photo, caption=caption)
        await hell.delete()
    except ChatSendMediaForbidden:
        await hell.edit(caption, disable_web_page_preview=True)

    if os.path.exists(photo):
        os.remove(photo)


@on_message("airing", allow_stan=True)
async def airing(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(message, "Give me an anime name to search!")

    query = await hellbot.input(message)
    hell = await hellbot.edit(message, "Searching ...")
    caption, photo = await get_airing_info(query)

    try:
        await message.reply_photo(photo, caption=caption)
        await hell.delete()
    except ChatSendMediaForbidden:
        await hell.edit(caption, disable_web_page_preview=True)

    if os.path.exists(photo):
        os.remove(photo)


@on_message(["anilistuser", "aniuser"], allow_stan=True)
async def anilist_user(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(message, "Give me an anilist username to search!")

    query = await hellbot.input(message)
    hell = await hellbot.edit(message, "Searching ...")
    caption, photo = await get_anilist_user_info(query)

    try:
        await message.reply_photo(photo, caption=caption)
        await hell.delete()
    except ChatSendMediaForbidden:
        await hell.edit(caption, disable_web_page_preview=True)

    if os.path.exists(photo):
        os.remove(photo)


@on_message(["filler", "canon"], allow_stan=True)
async def fillers(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(message, "Give me an anime name to search!")

    query = await hellbot.input(message)
    hell = await hellbot.edit(message, "Searching ...")

    caption = await get_filler_info(query)
    if caption == "":
        return await hellbot.delete(hell, "No results found!")

    await hell.edit(caption, disable_web_page_preview=True)


@on_message("watchorder", allow_stan=True)
async def watch_order(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(message, "Give me an anime name to search!")

    query = await hellbot.input(message)
    hell = await hellbot.edit(message, "Searching ...")

    caption = await get_watch_order(query)
    if caption == "":
        return await hellbot.delete(hell, "No results found!")

    await hell.edit(caption, disable_web_page_preview=True)


HelpMenu("anime").add(
    "anime",
    "<name>",
    "Get a detailed information about the mentioned anime.",
    "anime one piece",
).add(
    "manga",
    "<name>",
    "Get a detailed information about the mentioned manga.",
    "manga one piece",
).add(
    "character",
    "<name>",
    "Get a detailed information about the mentioned character.",
    "character monkey d luffy",
).add(
    "airing",
    "<name>",
    "Get a detailed airing information about the mentioned anime.",
    "airing one piece",
).add(
    "anilistuser",
    "<username>",
    "Get a detailed information about the mentioned anilist user.",
    "anilistuser meizhellboy",
    "You can also use 'aniuser' as alias",
).add(
    "filler",
    "<name>",
    "Get the list of filler/canon episodes about the mentioned anime.",
    "filler one piece",
    "You can also use 'canon' as alias",
).add(
    "watchorder",
    "<name>",
    "Get the watch order about the mentioned anime.",
    "watchorder one piece",
).info(
    "Anime Menu"
).done()
