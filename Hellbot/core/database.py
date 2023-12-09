import datetime
import time

from motor import motor_asyncio
from motor.core import AgnosticClient

from .config import Config, Symbols
from .logger import LOGS


class Database:
    def __init__(self, uri: str) -> None:
        self.client: AgnosticClient = motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self.client["Hellbot"]

        self.afk = self.db["afk"]
        self.antiflood = self.db["antiflood"]
        self.autopost = self.db["autopost"]
        self.blacklist = self.db["blacklist"]
        self.echo = self.db["echo"]
        self.env = self.db["env"]
        self.filter = self.db["filter"]
        self.gban = self.db["gban"]
        self.session = self.db["session"]
        self.stan_users = self.db["stan_users"]

    async def connect(self):
        try:
            await self.client.admin.command("ping")
            LOGS.info(
                f"{Symbols.bullet * 3} Database Connection Established! {Symbols.bullet * 3}"
            )
        except Exception as e:
            LOGS.info(f"{Symbols.cross_mark} DatabaseErr: {e} ")
            quit(1)

    def get_datetime(self) -> str:
        return datetime.datetime.now().strftime("%d/%m/%Y - %H:%M")

    async def set_env(self, name: str, value: str) -> None:
        await self.env.update_one(
            {"name": name}, {"$set": {"value": value}}, upsert=True
        )

    async def get_env(self, name: str) -> str | None:
        if await self.is_env(name):
            data = await self.env.find_one({"name": name})
            return data["value"]
        return None

    async def rm_env(self, name: str) -> None:
        await self.env.delete_one({"name": name})

    async def is_env(self, name: str) -> bool:
        if await self.env.find_one({"name": name}):
            return True
        return False

    async def get_all_env(self) -> list:
        return [i async for i in self.env.find({})]

    async def is_stan(self, user_id: int) -> bool:
        if await self.stan_users.find_one({"user_id": user_id}):
            return True
        return False

    async def add_stan(self, user_id: int) -> bool:
        if await self.is_stan(user_id):
            return False
        await self.stan_users.insert_one(
            {"user_id": user_id, "date": self.get_datetime()}
        )
        return True

    async def rm_stan(self, user_id: int) -> bool:
        if not await self.is_stan(user_id):
            return False
        await self.stan_users.delete_one({"user_id": user_id})
        return True

    async def get_stans(self) -> list:
        return [i async for i in self.stan_users.find({})]

    async def is_session(self, user_id: int) -> bool:
        if await self.session.find_one({"user_id": user_id}):
            return True
        return False

    async def update_session(self, user_id: int, session: str) -> None:
        await self.session.update_one(
            {"user_id": user_id},
            {"$set": {"session": session, "date": self.get_datetime()}},
            upsert=True,
        )

    async def rm_session(self, user_id: int) -> None:
        await self.session.delete_one({"user_id": user_id})

    async def get_session(self, user_id: int):
        if not await self.is_session(user_id):
            return False
        data = await self.session.find_one({"user_id": user_id})
        return data

    async def get_all_sessions(self) -> list:
        return [i async for i in self.session.find({})]

    async def is_gbanned(self, user_id: int) -> bool:
        if await self.gban.find_one({"user_id": user_id}):
            return True
        return False

    async def add_gban(self, user_id: int, reason: str) -> bool:
        if await self.is_gbanned(user_id):
            return False
        await self.gban.insert_one(
            {"user_id": user_id, "reason": reason, "date": self.get_datetime()}
        )
        return True

    async def rm_gban(self, user_id: int) -> bool:
        if not await self.is_gbanned(user_id):
            return False
        await self.gban.delete_one({"user_id": user_id})
        return True

    async def get_gban(self) -> list:
        return [i async for i in self.gban.find({})]

    async def set_afk(
        self, user_id: int, reason: str, media: str, media_type: str
    ) -> None:
        await self.afk.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "reason": reason,
                    "time": time.time(),
                    "media": media,
                    "media_type": media_type,
                }
            },
            upsert=True,
        )

    async def get_afk(self, user_id: int):
        data = await self.afk.find_one({"user_id": user_id})
        return data

    async def is_afk(self, user_id: int) -> bool:
        if await self.afk.find_one({"user_id": user_id}):
            return True
        return False

    async def rm_afk(self, user_id: int) -> None:
        await self.afk.delete_one({"user_id": user_id})

    async def set_flood(self, client_chat: tuple[int, int], settings: dict):
        await self.antiflood.update_one(
            {"client": client_chat[0], "chat": client_chat[1]},
            {"$set": settings},
            upsert=True,
        )

    async def get_flood(self, client_chat: tuple[int, int]):
        data = await self.antiflood.find_one(
            {"client": client_chat[0], "chat": client_chat[1]}
        )
        return data or {}

    async def is_flood(self, client_chat: tuple[int, int]) -> bool:
        data = await self.get_flood(client_chat)

        if not data:
            return False

        if data["limit"] == 0:
            return False

        return True

    async def get_all_floods(self) -> list:
        return [i async for i in self.antiflood.find({})]

    async def set_autopost(self, client: int, from_channel: int, to_channel: int):
        await self.autopost.update_one(
            {"client": client},
            {
                "$push": {
                    "autopost": {
                        "from_channel": from_channel,
                        "to_channel": to_channel,
                        "date": self.get_datetime(),
                    }
                }
            },
            upsert=True,
        )

    async def get_autopost(self, client: int, from_channel: int):
        data = await self.autopost.find_one(
            {
                "client": client,
                "autopost": {"$elemMatch": {"from_channel": from_channel}},
            }
        )
        return data

    async def is_autopost(
        self, client: int, from_channel: int, to_channel: int = None
    ) -> bool:
        if to_channel:
            data = await self.autopost.find_one(
                {
                    "client": client,
                    "autopost": {
                        "$elemMatch": {
                            "from_channel": from_channel,
                            "to_channel": to_channel,
                        }
                    },
                }
            )
        else:
            data = await self.autopost.find_one(
                {
                    "client": client,
                    "autopost": {"$elemMatch": {"from_channel": from_channel}},
                }
            )
        return True if data else False

    async def rm_autopost(self, client: int, from_channel: int, to_channel: int):
        await self.autopost.update_one(
            {"client": client},
            {
                "$pull": {
                    "autopost": {
                        "from_channel": from_channel,
                        "to_channel": to_channel,
                    }
                }
            },
        )

    async def get_all_autoposts(self, client: int) -> list:
        return [i async for i in self.autopost.find({"client": client})]

    async def add_blacklist(self, client: int, chat: int, blacklist: str):
        await self.blacklist.update_one(
            {"client": client, "chat": chat},
            {"$push": {"blacklist": blacklist}},
            upsert=True,
        )

    async def rm_blacklist(self, client: int, chat: int, blacklist: str):
        await self.blacklist.update_one(
            {"client": client, "chat": chat},
            {"$pull": {"blacklist": blacklist}},
        )

    async def is_blacklist(self, client: int, chat: int, blacklist: str) -> bool:
        blacklists = await self.get_all_blacklists(client, chat)
        if blacklist in blacklists:
            return True
        return False

    async def get_all_blacklists(self, client: int, chat: int) -> list:
        data = await self.blacklist.find_one({"client": client, "chat": chat})

        if not data:
            return []

        return data["blacklist"]

    async def get_blacklist_clients(self) -> list:
        return [i async for i in self.blacklist.find({})]

    async def set_echo(self, client: int, chat: int, user: int):
        await self.echo.update_one(
            {"client": client, "chat": chat},
            {"$push": {"echo": user}},
            upsert=True,
        )

    async def rm_echo(self, client: int, chat: int, user: int):
        await self.echo.update_one(
            {"client": client, "chat": chat},
            {"$pull": {"echo": user}},
        )

    async def is_echo(self, client: int, chat: int, user: int) -> bool:
        data = await self.get_all_echo(client, chat)
        if user in data:
            return True
        return False

    async def get_all_echo(self, client: int, chat: int) -> list:
        data = await self.echo.find_one({"client": client, "chat": chat})

        if not data:
            return []

        return data["echo"]

    async def set_filter(
        self, client: int, chat: int, keyword: str, fileId: str = None, text: str = None
    ):
        await self.filter.update_one(
            {"client": client, "chat": chat},
            {"$push": {"filter": {"keyword": keyword, "fileId": fileId, "text": text}}},
            upsert=True,
        )

    async def rm_filter(self, client: int, chat: int, keyword: str):
        await self.filter.update_one(
            {"client": client, "chat": chat},
            {"$pull": {"filter": {"keyword": keyword}}},
        )

    async def rm_all_filters(self, client: int, chat: int):
        await self.filter.delete_one({"client": client, "chat": chat})

    async def is_filter(self, client: int, chat: int, keyword: str) -> bool:
        data = await self.get_filter(client, chat, keyword)
        return True if data else False

    async def get_filter(self, client: int, chat: int, keyword: str):
        data = await self.filter.find_one(
            {
                "client": client,
                "chat": chat,
                "filter": {"$elemMatch": {"keyword": keyword}},
            }
        )
        return data

    async def get_all_filters(self, client: int, chat: int) -> list:
        data = await self.filter.find_one({"client": client, "chat": chat})

        if not data:
            return []

        return data["filter"]


db = Database(Config.DATABASE_URL)
