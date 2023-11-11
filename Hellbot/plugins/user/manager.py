from pyrogram.types import Message

from Hellbot.core import Symbols, db, hellbot
from Hellbot.core.config import all_env

from . import on_message


@on_message("getvar", allow_sudo=True)
async def getvar(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(message, "Give a varname to fetch value.")

    varname = message.command[1]
    value = await db.get_env(varname.upper())

    if isinstance(value, str):
        await hellbot.edit(
            message,
            f"{Symbols.anchor} **𝖵𝖺𝗋𝗂𝖺𝖻𝗅𝖾 𝖭𝖺𝗆𝖾:** `{varname.upper()}`\n{Symbols.anchor} **𝖵𝖺𝗅𝗎𝖾:** `{value}`",
        )
    elif value is None:
        await hellbot.delete(message, f"**𝖵𝖺𝗋𝗂𝖺𝖻𝗅𝖾 {varname} 𝖽𝗈𝖾𝗌 𝗇𝗈𝗍 𝖾𝗑𝗂𝗌𝗍𝗌!**")


@on_message("getallvar", allow_sudo=True)
async def getallvar(_, message: Message):
    text = "**𝖫𝗂𝗌𝗍 𝗈𝖿 𝖺𝗅𝗅 𝖣𝖡 𝗏𝖺𝗋𝗂𝖺𝖻𝗅𝖾 𝖺𝗋𝖾:**\n\n"
    for env in all_env:
        text += f"   {Symbols.anchor} `{env}`\n"
    await hellbot.edit(message, text)


@on_message("setvar", allow_sudo=True)
async def setvar(_, message: Message):
    if len(message.command) < 3:
        return await hellbot.delete(
            message, "**𝖦𝗂𝗏𝖾 𝗏𝖺𝗋𝗇𝖺𝗆𝖾 𝖺𝗇𝖽 𝗏𝖺𝗋-𝗏𝖺𝗅𝗎𝖾 𝖺𝗅𝗈𝗇𝗀 𝗐𝗂𝗍𝗁 𝗍𝗁𝖾 𝖼𝗈𝗆𝗆𝖺𝗇𝖽!**"
        )

    input = await hellbot.input(message)
    varname = input.split(" ", 1)[0]
    varvalue = input.split(" ", 1)[1]
    await db.set_env(varname.upper(), varvalue)
    await hellbot.delete(
        message,
        f"**𝖵𝖺𝗋𝗂𝖺𝖻𝗅𝖾** `{varname.upper()}` **𝗌𝖾𝗍𝗎𝗉 𝖼𝗈𝗆𝗉𝗅𝖾𝗍𝖾!**\n\n**𝖵𝖺𝗅𝗎𝖾:** `{varvalue}`",
    )


@on_message("delvar", allow_sudo=True)
async def delvar(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(message, "**𝖦𝗂𝗏𝖾 𝗏𝖺𝗋𝗇𝖺𝗆𝖾 𝖺𝗅𝗈𝗇𝗀 𝗐𝗂𝗍𝗁 𝗍𝗁𝖾 𝖼𝗈𝗆𝗆𝖺𝗇𝖽!**")

    varname = message.command[1]
    if await db.is_env(varname.upper()):
        await db.rm_env(varname.upper())
        await hellbot.delete(
            message, f"**𝖵𝖺𝗋𝗂𝖺𝖻𝗅𝖾** `{varname.upper()}` **𝖽𝖾𝗅𝖾𝗍𝖾𝖽 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒!**"
        )
        return

    await hellbot.delete(message, "**𝖭𝗈 𝗌𝗎𝖼𝗁 𝗏𝖺𝗋𝗂𝖺𝖻𝗅𝖾 𝖿𝗈𝗎𝗇𝖽 𝗂𝗇 𝖽𝖺𝗍𝖺𝖻𝖺𝗌𝖾 𝗍𝗈 𝖽𝖾𝗅𝖾𝗍𝖾!**")
