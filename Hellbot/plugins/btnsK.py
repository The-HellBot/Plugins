# K: Keyboard Buttons

from pyrogram.types import KeyboardButton, ReplyKeyboardMarkup


def gen_keyboard(collection: list, row: int = 2) -> list[list[KeyboardButton]]:
    keyboard = []
    for i in range(0, len(collection), row):
        kyb = []
        for x in collection[i : i + row]:
            kyb.append(KeyboardButton(x))
        keyboard.append(kyb)
    return keyboard


SETTINGS_KB = ReplyKeyboardMarkup(
    [
        [KeyboardButton("Clients 👥")],
        [KeyboardButton("Home 🏠")],
    ],
    resize_keyboard=True,
)
