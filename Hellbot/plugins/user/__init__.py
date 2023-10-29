from Hellbot.core.clients import hellbot
from Hellbot.core.config import Config
from Hellbot.plugins.decorator import on_message
from Hellbot.plugins.help import HelpMenu

handler = Config.HANDLERS[0]
bot = hellbot.bot
