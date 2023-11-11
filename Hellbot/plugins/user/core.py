from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from Hellbot.core import Config, Symbols, hellbot

from .. import REPO_TEXT
from . import HelpMenu, bot, handler, on_message


@on_message("help", allow_sudo=True)
async def help(client: Client, message: Message):
    hell = await hellbot.edit(message, "**Processing...**")
    if len(message.command) == 1:
        try:
            result = await client.get_inline_bot_results(bot.me.username, "help_menu")
            await client.send_inline_bot_result(
                message.chat.id,
                result.query_id,
                result.results[0].id,
                True,
            )
            return await hell.delete()
        except Exception as e:
            await hellbot.error(hell, str(e), 20)
            return

    plugin = await hellbot.input(message)
    if plugin.lower() in Config.CMD_MENU:
        try:
            await hellbot.edit(hell, Config.CMD_MENU[plugin.lower()])
            return
        except Exception as e:
            await hellbot.error(hell, str(e), 20)
            return

    available_plugins = f"{Symbols.bullet} **𝖠𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 𝗉𝗅𝗎𝗀𝗂𝗇𝗌:**\n\n"
    for i in Config.CMD_MENU.keys():
        available_plugins += f"`{i}`, "
    available_plugins = available_plugins[:-2]
    available_plugins += (
        f"\n\n𝖣𝗈 `{handler}help <plugin name>` 𝗍𝗈 𝗀𝖾𝗍 𝖽𝖾𝗍𝖺𝗂𝗅𝖾𝖽 𝗂𝗇𝖿𝗈 𝗈𝖿 𝗍𝗁𝖺𝗍 𝗉𝗅𝗎𝗀𝗂𝗇."
    )
    await hellbot.edit(hell, available_plugins, ParseMode.MARKDOWN)


@on_message("repo", allow_sudo=True)
async def repo(_, message: Message):
    await hellbot.edit(message, REPO_TEXT, no_link_preview=True)


@on_message("plinfo", allow_sudo=True)
async def plugin_info(_, message: Message):
    plugin = await hellbot.input(message)
    if plugin.lower() in Config.CMD_MENU:
        try:
            await hellbot.edit(message, Config.CMD_MENU[plugin.lower()])
            return
        except Exception as e:
            await hellbot.error(message, str(e), 20)
            return
    await hellbot.error(message, f"**Invalid Plugin Name:** `{plugin}`", 20)


@on_message("cmdinfo", allow_sudo=True)
async def command_info(_, message: Message):
    cmd = await hellbot.input(message)
    if cmd.lower() in Config.CMD_INFO:
        try:
            await hellbot.edit(message, Config.CMD_INFO[cmd.lower()])
            return
        except Exception as e:
            await hellbot.error(message, str(e), 20)
            return
    await hellbot.error(message, f"**Invalid Command Name:** `{cmd}`", 20)


HelpMenu("help").add(
    "help",
    "<plugin name>",
    "Get the detailed help menu for that mentioned plugin or get the whole help menu instead.",
    "help alive",
).add(
    "repo", None, "Get the repo link of the bot.", "repo"
).add(
    "plinfo",
    "<plugin name>",
    "Get the detailed info of the mentioned plugin.",
    "plinfo alive",
).add(
    "cmdinfo",
    "<command name>",
    "Get the detailed info of the mentioned command.",
    "cmdinfo alive",
).info(
    "Help Menu"
).done()
