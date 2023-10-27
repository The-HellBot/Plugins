from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()


class Config:
    # editable configs
    API_HASH = getenv("API_HASH", None)
    API_ID = int(getenv("API_ID", 0))
    BOT_TOKEN = getenv("BOT_TOKEN", None)
    DATABASE_URL = getenv("DATABASE_URL", None)
    HANDLERS = getenv("HANDLERS", ". ! ?").strip().split()
    LOGGER_ID = int(getenv("LOGGER_ID", 0))
    OWNER_ID = int(getenv("OWNER_ID", 0))

    # storage dir: you may or may not edit
    DWL_DIR = "./downloads/"
    TEMP_DIR = "./temp/"

    # users config: do not edit
    AUTH_USERS = filters.user()
    BANNED_USERS = filters.user()
    SUDO_USERS = filters.user()

    # Global config: do not edit
    HELP_DICT = {}
    CMD_MENU = {}
    CMD_INFO = {}


class Limits:
    AdminRoleLength = 16
    AdminsLimit = 50
    BioLength = 70
    BotDescriptionLength = 512
    BotInfoLength = 120
    BotsLimit = 20
    CaptionLength = 1024
    ChannelGroupsLimit = 500
    ChatTitleLength = 128
    FileNameLength = 60
    MessageLength = 4096
    NameLength = 64
    PremiumBioLength = 140
    PremiumCaptionLength = 2048
    PremiumChannelGroupsLimit = 1000
    StickerAniamtedLimit = 50
    StickerPackNameLength = 64
    StickerStaticLimit = 120


class Symbols:
    arrow_left = "«"
    arrow_right = "»"
    bullet = "•"
    check_mark = "✔"
    cross_mark = "✘"
    diamond_1 = "◇"
    diamond_2 = "◈"
    radio_select = "◉"
    radio_unselect = "〇"


all_configs = {
    key: value for key, value in Config.__dict__.items() if not key.startswith("__")
}
