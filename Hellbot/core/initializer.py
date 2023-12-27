from .clients import hellbot
from .config import Config, Symbols
from .database import db
from .logger import LOGS


async def _AuthUsers() -> None:
    temp_list = []
    temp_list.append(Config.OWNER_ID)
    temp_list.extend([(await client.get_me()).id for client in hellbot.users])

    stan_users = await db.get_all_stans()
    for user in stan_users:
        temp_list.append(user["user_id"])

    users = list(set(temp_list))
    for user in users:
        Config.AUTH_USERS.add(user)

    temp_list = None
    LOGS.info(
        f"{Symbols.arrow_right * 2} Added Authorized Users {Symbols.arrow_left * 2}"
    )


async def _StanUsers() -> None:
    users = await db.get_all_stans()
    for user in users:
        Config.STAN_USERS.add(user["user_id"])

    LOGS.info(f"{Symbols.arrow_right * 2} Added Stan Users {Symbols.arrow_left * 2}")


async def _GbanUsers() -> None:
    users = await db.get_gban()
    for user in users:
        Config.BANNED_USERS.add(user["user_id"])

    LOGS.info(
        f"{Symbols.arrow_right * 2} Added {len(users)} Gbanned Users {Symbols.arrow_left * 2}"
    )

    musers = await db.get_gmute()
    for user in musers:
        Config.MUTED_USERS.add(user["user_id"])

    LOGS.info(
        f"{Symbols.arrow_right * 2} Added {len(musers)} Gmuted Users {Symbols.arrow_left * 2}"
    )


async def UserSetup() -> None:
    """Initialize Users Config"""
    LOGS.info(f"{Symbols.bullet * 3} Setting Up Users {Symbols.bullet * 3}")
    await _AuthUsers()
    await _StanUsers()
    await _GbanUsers()


async def ForcesubSetup() -> None:
    """Initialize Forcesub Config"""
    chats = await db.get_all_forcesubs()
    for chat in chats:
        if chat not in Config.FORCESUBS:
            Config.FORCESUBS.add(chat["chat"])
