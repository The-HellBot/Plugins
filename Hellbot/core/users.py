from .clients import hellbot
from .config import Config, Symbols
from .database import db
from .logger import LOGS


class Users:
    async def AuthUsers(self):
        temp_list = []
        temp_list.append(Config.OWNER_ID)
        temp_list.extend(await db.get_stans())
        temp_list.extend([(await client.get_me()).id for client in hellbot.users])
        users = list(set(temp_list))
        for user in users:
            Config.AUTH_USERS.add(user)
        temp_list = None
        LOGS.info(
            f"{Symbols.arrow_right * 2} Added Authorized Users {Symbols.arrow_left * 2}"
        )

    async def StanUsers(self):
        users = await db.get_stans()
        for user in users:
            Config.STAN_USERS.add(user)
        LOGS.info(
            f"{Symbols.arrow_right * 2} Added Stan Users {Symbols.arrow_left * 2}"
        )

    async def GbanUsers(self):
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

    async def setup(self):
        LOGS.info(f"{Symbols.bullet * 3} Setting Up Users {Symbols.bullet * 3}")
        await self.AuthUsers()
        await self.StanUsers()
        await self.GbanUsers()
