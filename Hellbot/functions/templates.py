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

ANIME_TEMPLATES = [
    """
{name}

╭────────────────•
╰➢ **𝖲𝖼𝗈𝗋𝖾:** `{score}`
╰➢ **𝖲𝗈𝗎𝗋𝖼𝖾:** `{source}`
╰➢ **𝖳𝗒𝗉𝖾:** `{mtype}`
╰➢ **𝖤𝗉𝗂𝗌𝗈𝖽𝖾𝗌:** `{episodes}`
╰➢ **𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇:** `{duration} minutes`
╰➢ **𝖲𝗍𝖺𝗍𝗎𝗌:** `{status}`
╰➢ **𝖥𝗈𝗋𝗆𝖺𝗍:** `{format}`
╰➢ **𝖦𝖾𝗇𝗋𝖾:** `{genre}`
╰➢ **𝖲𝗍𝗎𝖽𝗂𝗈:** `{studio}`
╰➢ **𝖳𝗋𝖺𝗂𝗅𝖾𝗋:** {trailer}
╰➢ **𝖶𝖾𝖻𝗌𝗂𝗍𝖾:** {siteurl}
╰────────────────•
"""
]

MANGA_TEMPLATES = [
    """
{name}

╭────────────────•
╰➢ **𝖲𝖼𝗈𝗋𝖾:** `{score}`
╰➢ **𝖲𝗈𝗎𝗋𝖼𝖾:** `{source}`
╰➢ **𝖳𝗒𝗉𝖾:** `{mtype}`
╰➢ **𝖢𝗁𝖺𝗉𝗍𝖾𝗋𝗌:** `{chapters}`
╰➢ **𝖵𝗈𝗅𝗎𝗆𝖾𝗌:** `{volumes}`
╰➢ **𝖲𝗍𝖺𝗍𝗎𝗌:** `{status}`
╰➢ **𝖥𝗈𝗋𝗆𝖺𝗍:** `{format}`
╰➢ **𝖦𝖾𝗇𝗋𝖾:** `{genre}`
╰➢ **𝖶𝖾𝖻𝗌𝗂𝗍𝖾:** {siteurl}
╰────────────────•
"""
]

CHARACTER_TEMPLATES = [
    """
{name}

╭────────────────•
╰➢ **𝖦𝖾𝗇𝖽𝖾𝗋:** `{gender}`
╰➢ **𝖣𝖺𝗍𝖾 𝗈𝖿 𝖡𝗂𝗋𝗍𝗁:** `{date_of_birth}`
╰➢ **𝖠𝗀𝖾:** `{age}`
╰➢ **𝖡𝗅𝗈𝗈𝖽 𝖳𝗒𝗉𝖾:** `{blood_type}`
╰➢ **𝖥𝖺𝗏𝗈𝗎𝗋𝗂𝗍𝖾𝗌:** `{favourites}`
╰➢ **𝖶𝖾𝖻𝗌𝗂𝗍𝖾:** {siteurl}{role_in}
╰────────────────•
{description}
"""
]

AIRING_TEMPLATES = [
    """
{name}

╭────────────────•
╰➢ **𝖲𝗍𝖺𝗍𝗎𝗌:** `{status}`
╰➢ **𝖤𝗉𝗂𝗌𝗈𝖽𝖾:** `{episode}`
╰────────────────•{airing_info}
"""
]


ANILIST_USER_TEMPLATES = [
    """
**💫 {name}**

╭──── 𝖠𝗇𝗂𝗆𝖾 ─────•
╰➢ **𝖢𝗈𝗎𝗇𝗍:** `{anime_count}`
╰➢ **𝖲𝖼𝗈𝗋𝖾:** `{anime_score}`
╰➢ **𝖬𝗂𝗇𝗎𝗍𝖾𝗌 𝖲𝗉𝖾𝗇𝗍:** `{minutes}`
╰➢ **𝖤𝗉𝗂𝗌𝗈𝖽𝖾𝗌 𝖶𝖺𝗍𝖼𝗁𝖾𝖽:** `{episodes}`
╰────────────────•
╭──── 𝖬𝖺𝗇𝗀𝖺 ─────•
╰➢ **𝖢𝗈𝗎𝗇𝗍:** `{manga_count}`
╰➢ **𝖲𝖼𝗈𝗋𝖾:** `{manga_score}`
╰➢ **𝖢𝗁𝖺𝗉𝗍𝖾𝗋𝗌:** `{chapters}`
╰➢ **𝖵𝗈𝗅𝗎𝗆𝖾𝗌:** `{volumes}`
╰────────────────•

𝖶𝖾𝖻𝗌𝗂𝗍𝖾: {siteurl}
"""
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


async def anime_template(
    name: str,
    score: str,
    source: str,
    mtype: str,
    episodes: str,
    duration: str,
    status: str,
    format: str,
    genre: str,
    studio: str,
    trailer: str,
    siteurl: str,
) -> str:
    template = await db.get_env(ENV.anime_template)
    if template:
        message = template
    else:
        message = random.choice(ANIME_TEMPLATES)
    return message.format(
        name=name,
        score=score,
        source=source,
        mtype=mtype,
        episodes=episodes,
        duration=duration,
        status=status,
        format=format,
        genre=genre,
        studio=studio,
        trailer=trailer,
        siteurl=siteurl,
    )


async def manga_templates(
    name: str,
    score: str,
    source: str,
    mtype: str,
    chapters: str,
    volumes: str,
    status: str,
    format: str,
    genre: str,
    siteurl: str,
) -> str:
    template = await db.get_env(ENV.manga_template)
    if template:
        message = template
    else:
        message = random.choice(MANGA_TEMPLATES)
    return message.format(
        name=name,
        score=score,
        source=source,
        mtype=mtype,
        chapters=chapters,
        volumes=volumes,
        status=status,
        format=format,
        genre=genre,
        siteurl=siteurl,
    )


async def character_templates(
    name: str,
    gender: str,
    date_of_birth: str,
    age: str,
    blood_type: str,
    favourites: str,
    siteurl: str,
    role_in: str,
    description: str,
) -> str:
    template = await db.get_env(ENV.character_template)
    if template:
        message = template
    else:
        message = random.choice(CHARACTER_TEMPLATES)
    return message.format(
        name=name,
        gender=gender,
        date_of_birth=date_of_birth,
        age=age,
        blood_type=blood_type,
        favourites=favourites,
        siteurl=siteurl,
        role_in=role_in,
        description=description,
    )


async def airing_templates(
    name: str,
    status: str,
    episode: str,
    airing_info: str,
) -> str:
    template = await db.get_env(ENV.airing_template)
    if template:
        message = template
    else:
        message = random.choice(AIRING_TEMPLATES)
    return message.format(
        name=name,
        status=status,
        episode=episode,
        airing_info=airing_info,
    )


async def anilist_user_templates(
    name: str, anime: tuple, manga: tuple, siteurl: str
) -> str:
    template = await db.get_env(ENV.anilist_user_template)
    if template:
        message = template
    else:
        message = random.choice(ANILIST_USER_TEMPLATES)
    return message.format(
        name=name,
        anime_count=anime[0],
        anime_score=anime[1],
        minutes=anime[2],
        episodes=anime[3],
        manga_count=manga[0],
        manga_score=manga[1],
        chapters=manga[2],
        volumes=manga[3],
        siteurl=siteurl,
    )
