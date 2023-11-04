from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from Hellbot.core import Config, Symbols, hellbot

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


HelpMenu("help").add(
    "help",
    "<plugin name>",
    "Get the detailed help menu for that mentioned plugin or get the whole help menu instead.",
    "help alive",
).info("Help Menu").done()
