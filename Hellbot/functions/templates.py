import random

from Hellbot import __version__
from Hellbot.core import ENV, db

ALIVE_TEMPLATES = [
    (
        "•────────────────•\n"
        "•       𝐇ᴇʟʟ𝐁ᴏᴛ 𝐈s 𝐀ʟɪᴠᴇ        •\n"
        "╭────────────────•\n"
        "╰➢ ᴏᴡɴᴇʀ » {owner}\n"
        "╰➢ ᴘʏʀᴏɢʀᴀᴍ » {pyrogram}\n"
        "╰➢ ʜᴇʟʟʙᴏᴛ » {hellbot}\n"
        "╰➢ ᴘʏᴛʜᴏɴ » {python}\n"
        "╰➢ ᴜᴘᴛɪᴍᴇ » {uptime}\n"
        "╰────────────────•\n"
        "𝖡𝗒 © @HellBot_Networks\n"
        "•────────────────•\n"
    ),
]

PING_TEMPLATES = [
    """**🍀 𝖯𝗂𝗇𝗀!**

    ⚘  **ѕρєє∂:** {speed} m/s
    ⚘  **υρтιмє:** {uptime}
    ⚘  **σωηєя:** {owner}""",
]

HELP_MENU_TEMPLATES = [
    """**🍀 𝖧𝖾𝗅𝗉 𝖬𝖾𝗇𝗎 𝖿𝗈𝗋:** {owner}

__📃 𝖫𝗈𝖺𝖽𝖾𝖽__ **{plugins} 𝗉𝗅𝗎𝗀𝗂𝗇𝗌** __𝗐𝗂𝗍𝗁 𝖺 𝗍𝗈𝗍𝖺𝗅 𝗈𝖿__ **{commands} 𝖼𝗈𝗆𝗆𝖺𝗇𝖽𝗌.**

**📑 Page:** __{current}/{last}__""",
]

COMMAND_MENU_TEMPLATES = [
    """**𝖯𝗅𝗎𝗀𝗂𝗇 𝖥𝗂𝗅𝖾:** `{file}`
**𝖯𝗅𝗎𝗀𝗂𝗇 𝖨𝗇𝖿𝗈:** __{info} 🍀__

**📃 𝖫𝗈𝖺𝖽𝖾𝖽 𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌:** `{commands}`""",
]


async def alive_template(owner: str, uptime: str) -> str:
    template = await db.get_env(ENV.alive_template)
    if template:
        message = template
    else:
        message = random.choice(ALIVE_TEMPLATES)
    return message.format(
        owner=owner,
        pyrogram=__version__["pyrogram"],
        hellbot=__version__["hellbot"],
        python=__version__["python"],
        uptime=uptime,
    )


async def ping_template(speed: float, uptime: str, owner: str) -> str:
    template = await db.get_env(ENV.ping_template)
    if template:
        message = template
    else:
        message = random.choice(PING_TEMPLATES)
    return message.format(speed=speed, uptime=uptime, owner=owner)


async def help_template(
    owner: str, cmd_n_plgn: tuple[int, int], page: tuple[int, int]
) -> str:
    template = await db.get_env(ENV.help_template)
    if template:
        message = template
    else:
        message = random.choice(HELP_MENU_TEMPLATES)
    return message.format(
        owner=owner,
        commands=cmd_n_plgn[0],
        plugins=cmd_n_plgn[1],
        current=page[0],
        last=page[1],
    )


async def command_template(file: str, info: str, commands: str) -> str:
    template = await db.get_env(ENV.command_template)
    if template:
        message = template
    else:
        message = random.choice(COMMAND_MENU_TEMPLATES)
    return message.format(file=file, info=info, commands=commands)
