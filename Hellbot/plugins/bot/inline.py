from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

from Hellbot.functions.templates import help_template

from ..btnsG import gen_inline_help_buttons
from . import Config, hellbot


@hellbot.bot.on_inline_query(filters.regex(r"help_menu"))
async def help_inline(_, query: InlineQuery):
    if not query.from_user.id in Config.AUTH_USERS:
        return
    no_of_plugins = len(Config.CMD_MENU)
    no_of_commands = len(Config.CMD_INFO)
    buttons, pages = await gen_inline_help_buttons(0, sorted(Config.CMD_MENU))
    caption = await help_template(
        query.from_user.mention, (no_of_commands, no_of_plugins), (1, pages)
    )
    await query.answer(
        results=[
            (
                InlineQueryResultArticle(
                    "HellBot Help Menu 🍀",
                    InputTextMessageContent(
                        caption,
                        disable_web_page_preview=True,
                    ),
                    description="Inline Query for Help Menu of HellBot",
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
            )
        ],
    )
