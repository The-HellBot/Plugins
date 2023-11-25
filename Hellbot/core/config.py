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
    CHROME_BIN = getenv("CHROME_BIN", "/app/.apt/usr/bin/google-chrome")

    # users config: do not edit
    AUTH_USERS = filters.user()
    BANNED_USERS = filters.user()
    STAN_USERS = filters.user()

    # Global config: do not edit
    BOT_CMD_INFO = {}
    BOT_CMD_MENU = {}
    BOT_HELP = {}

    CMD_INFO = {}
    CMD_MENU = {}
    HELP_DICT = {}

    AFK_CACHE = {}


class ENV:
    """ Database ENV Names """

    airing_template = "AIRING_TEMPLATE"
    airpollution_template = "AIRPOLLUTION_TEMPLATE"
    alive_pic = "ALIVE_PIC"
    alive_template = "ALIVE_TEMPLATE"
    anilist_user_template = "ANILIST_USER_TEMPLATE"
    anime_template = "ANIME_TEMPLATE"
    btn_in_help = "BUTTONS_IN_HELP"
    character_template = "CHARACTER_TEMPLATE"
    climate_api = "CLIMATE_API"
    climate_template = "CLIMATE_TEMPLATE"
    command_template = "COMMAND_TEMPLATE"
    help_emoji = "HELP_EMOJI"
    help_template = "HELP_TEMPLATE"
    is_logger = "IS_LOGGER"
    manga_template = "MANGA_TEMPLATE"
    ping_pic = "PING_PIC"
    ping_template = "PING_TEMPLATE"
    time_zone = "TIME_ZONE"
    unload_plugins = "UNLOAD_PLUGINS"


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
    anchor = "⚘"
    arrow_left = "«"
    arrow_right = "»"
    back = "🔙 back"
    bullet = "•"
    check_mark = "✔"
    close = "🗑️"
    cross_mark = "✘"
    diamond_1 = "◇"
    diamond_2 = "◈"
    next = "⤚ next"
    previous = "prev ⤙"
    radio_select = "◉"
    radio_unselect = "〇"
    triangle_left = "◂"
    triangle_right = "▸"


all_configs = {
    key: value for key, value in Config.__dict__.items() if not key.startswith("__")
}

all_env: list[str] = [value for key, value in ENV.__dict__.items() if not key.startswith("__")]
