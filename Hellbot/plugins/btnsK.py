# K: Keyboard Buttons

from pyrogram.types import KeyboardButton, ReplyKeyboardMarkup


SETTINGS_KB = ReplyKeyboardMarkup(
    [
        [KeyboardButton("Clients 👥")],
        [KeyboardButton("Home 🏠")],
    ]
)
