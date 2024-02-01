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

    # heroku related configs
    HEROKU_APPNAME = getenv("HEROKU_APPNAME", None)
    HEROKU_APIKEY = getenv("HEROKU_APIKEY", None)

    # github related configs
    PLUGINS_REPO = getenv("PLUGINS_REPO", "The-HellBot/Plugins")
    DEPLOY_REPO = getenv("DEPLOY_REPO", "The-HellBot/Hellbot")

    # storage dir: you may or may not edit
    DWL_DIR = "./downloads/"
    TEMP_DIR = "./temp/"
    CHROME_BIN = getenv("CHROME_BIN", "/app/.apt/usr/bin/google-chrome")
    CHROME_DRIVER = getenv("CHROME_DRIVER", "/app/.chromedriver/bin/chromedriver")
    FONT_PATH = "./Hellbot/resources/fonts/Montserrat.ttf"

    # users config: do not edit
    AUTH_USERS = filters.user()
    BANNED_USERS = filters.user()
    MUTED_USERS = filters.user()
    DEVS = filters.user([1432756163, 1874070588, 1533682758])
    STAN_USERS = filters.user()
    FORCESUBS = filters.chat()

    # Global config: do not edit
    BOT_CMD_INFO = {}
    BOT_CMD_MENU = {}
    BOT_HELP = {}

    CMD_INFO = {}
    CMD_MENU = {}
    HELP_DICT = {}

    AFK_CACHE = {}


class ENV:
    """Database ENV Names"""

    airing_template = "AIRING_TEMPLATE"
    airpollution_template = "AIRPOLLUTION_TEMPLATE"
    alive_pic = "ALIVE_PIC"
    alive_template = "ALIVE_TEMPLATE"
    anilist_user_template = "ANILIST_USER_TEMPLATE"
    anime_template = "ANIME_TEMPLATE"
    btn_in_help = "BUTTONS_IN_HELP"
    character_template = "CHARACTER_TEMPLATE"
    chat_info_template = "CHAT_INFO_TEMPLATE"
    climate_api = "CLIMATE_API"
    climate_template = "CLIMATE_TEMPLATE"
    command_template = "COMMAND_TEMPLATE"
    currency_api = "CURRENCY_API"
    custom_pmpermit = "CUSTOM_PMPERMIT"
    gban_template = "GBAN_TEMPLATE"
    github_user_template = "GITHUB_USER_TEMPLATE"
    help_emoji = "HELP_EMOJI"
    help_template = "HELP_TEMPLATE"
    is_logger = "IS_LOGGER"
    lyrics_api = "LYRICS_API"
    manga_template = "MANGA_TEMPLATE"
    ocr_api = "OCR_API"
    ping_pic = "PING_PIC"
    ping_template = "PING_TEMPLATE"
    pm_logger = "PM_LOGGER"
    pm_max_spam = "PM_MAX_SPAM"
    pmpermit = "PMPERMIT"
    pmpermit_pic = "PMPERMIT_PIC"
    remove_bg_api = "REMOVE_BG_API"
    thumbnail_url = "THUMBNAIL_URL"
    statistics_template = "STATISTICS_TEMPLATE"
    sticker_packname = "STICKER_PACKNAME"
    tag_logger = "TAG_LOGGER"
    telegraph_account = "TELEGRAPH_ACCOUNT"
    time_zone = "TIME_ZONE"
    unload_plugins = "UNLOAD_PLUGINS"
    unsplash_api = "UNSPLASH_API"
    usage_template = "USAGE_TEMPLATE"
    user_info_template = "USER_INFO_TEMPLATE"


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


os_configs = [
    "API_HASH",
    "API_ID",
    "BOT_TOKEN",
    "DATABASE_URL",
    "DEPLOY_REPO",
    "HANDLERS",
    "HEROKU_APIKEY",
    "HEROKU_APPNAME",
    "LOGGER_ID",
    "OWNER_ID",
    "PLUGINS_REPO",
]
all_env: list[str] = [
    value for key, value in ENV.__dict__.items() if not key.startswith("__")
]
