import datetime

from motor import motor_asyncio
from motor.core import AgnosticClient

from .config import Config, Symbols
from .logger import LOGS


class Database:
    def __init__(self, uri: str) -> None:
        self.client: AgnosticClient = motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self.client["Hellbot"]

        self.env = self.db["env"]
        self.gban = self.db["gban"]
        self.session = self.db["session"]
        self.sudo_users = self.db["sudo_users"]

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

    async def get_env(self, name: str) -> str:
        data = await self.env.find_one({"name": name})
        return data["value"]

    async def rm_env(self, name: str) -> None:
        await self.env.delete_one({"name": name})

    async def is_env(self, name: str) -> bool:
        if await self.env.find_one({"name": name}):
            return True
        return False

    async def get_all_env(self) -> list:
        return [i async for i in self.env.find({})]

    async def is_sudo(self, user_id: int) -> bool:
        if await self.sudo_users.find_one({"user_id": user_id}):
            return True
        return False

    async def add_sudo(self, user_id: int) -> bool:
        if await self.is_sudo(user_id):
            return False
        await self.sudo_users.insert_one(
            {"user_id": user_id, "date": self.get_datetime()}
        )
        return True

    async def rm_sudo(self, user_id: int) -> bool:
        if not await self.is_sudo(user_id):
            return False
        await self.sudo_users.delete_one({"user_id": user_id})
        return True

    async def get_sudos(self) -> list:
        return [i async for i in self.sudo_users.find({})]

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


db = Database(Config.DATABASE_URL)
