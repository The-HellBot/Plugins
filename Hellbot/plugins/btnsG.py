# G: Glass Buttons

from math import ceil

from pyrogram.types import InlineKeyboardButton

from Hellbot.core import ENV, Symbols, db


def gen_inline_keyboard(collection: list, row: int = 2) -> list[list[InlineKeyboardButton]]:
    keyboard = []
    for i in range(0, len(collection), row):
        kyb = []
        for x in collection[i : i + row]:
            button = btn(*x)
            kyb.append(button)
        keyboard.append(kyb)
    return keyboard


def btn(text, value, type="callback_data") -> InlineKeyboardButton:
    return InlineKeyboardButton(text, **{type: value})


async def gen_inline_help_buttons(page: int, plugins: list) -> tuple[list, int]:
    buttons = []
    column = await db.get_env(ENV.btn_in_help) or 5
    column = int(column)
    emoji = await db.get_env(ENV.help_emoji) or "✧"
    pairs = list(map(list, zip(plugins[::2], plugins[1::2])))

    if len(plugins) % 2 == 1:
        pairs.append([plugins[-1]])

    max_pages = ceil(len(pairs) / column)
    pairs = [pairs[i : i + column] for i in range(0, len(pairs), column)]

    for pair in pairs[page]:
        btn_pair = []
        for i, plugin in enumerate(pair):
            if i % 2 == 0:
                btn_pair.append(
                    InlineKeyboardButton(f"{emoji} {plugin}", f"help_menu:{page}:{plugin}")
                )
            else:
                btn_pair.append(
                    InlineKeyboardButton(f"{plugin} {emoji}", f"help_menu:{page}:{plugin}")
                )
        buttons.append(btn_pair)

    buttons.append(
        [
            InlineKeyboardButton(
                Symbols.previous, f"help_page:{(max_pages - 1) if page == 0 else (page - 1)}",
            ),
            InlineKeyboardButton(
                Symbols.close, "help_data:c"
            ),
            InlineKeyboardButton(
                Symbols.next, f"help_page:{0 if page == (max_pages - 1) else (page + 1)}",
            ),
        ]
    )

    return buttons, max_pages
