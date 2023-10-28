import glob
import importlib
import os
import sys
from pathlib import Path

import pyroaddon    # pylint: disable=unused-import
from pyrogram import Client
from pyrogram.types import Message

from .config import Config, Symbols
from .database import db
from .logger import LOGS


class HellClient(Client):
    def __init__(self) -> None:
        self.users: list[Client] = []
        self.bot: Client = Client(
            name="HellBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins=dict(root="Hellbot.plugins.bot"),
        )

    async def start_user(self) -> None:
        sessions = await db.get_all_sessions()
        for i, session in enumerate(sessions):
            try:
                client = Client(
                    name=f"HellUser#{i + 1}",
                    api_id=Config.API_ID,
                    api_hash=Config.API_HASH,
                    session_string=session["session"],
                )
                await client.start()
                me = await client.get_me()
                self.users.append(client)
                LOGS.info(
                    f"{Symbols.arrow_right * 2} Started User {i + 1}: '{me.first_name}' {Symbols.arrow_left * 2}"
                )
                is_in_logger = await self.validate_logger(client)
                if not is_in_logger:
                    LOGS.warning(
                        f"Client #{i+1}: '{me.first_name}' is not in Logger Group! Check and add manually for proper functioning."
                    )
            except Exception as e:
                LOGS.error(f"{i + 1}: {e}")
                continue

    async def start_bot(self) -> None:
        await self.bot.start()
        me = await self.bot.get_me()
        LOGS.info(
            f"{Symbols.arrow_right * 2} Started HellBot Client: '{me.username}' {Symbols.arrow_left * 2}"
        )

    async def load_plugin(self) -> None:
        files = glob.glob("Hellbot/plugins/user/*.py")
        count = 0
        for file in files:
            with open(file) as f:
                path = Path(f.name)
                shortname = path.stem.replace(".py", "")
                unload = await db.get_env("UNLOAD_PLUGINS")
                if unload and shortname in unload:
                    os.remove(Path(f"Hellbot/plugins/user/{shortname}.py"))
                    continue
                if shortname.startswith("__"):
                    continue
                fpath = Path(f"Hellbot/plugins/user/{shortname}.py")
                name = "Hellbot.plugins.user." + shortname
                spec = importlib.util.spec_from_file_location(name, fpath)
                load = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(load)
                sys.modules["Hellbot.plugins.user." + shortname] = load
                count += 1
            f.close()
        LOGS.info(
            f"{Symbols.bullet * 3} Loaded User Plugin: '{count}' {Symbols.bullet * 3}"
        )

    async def validate_logger(self, client: Client) -> bool:
        try:
            await client.get_chat_member(Config.LOGGER_ID, "me")
            return True
        except Exception:
            return await self.join_logger(client)

    async def join_logger(self, client: Client) -> bool:
        try:
            invite_link = await self.bot.export_chat_invite_link(Config.LOGGER_ID)
            await client.join_chat(invite_link)
            return True
        except Exception:
            return False

    async def startup(self) -> None:
        LOGS.info(
            f"{Symbols.bullet * 3} Starting HellBot Client & User {Symbols.bullet * 3}"
        )
        await self.start_bot()
        await self.start_user()
        await self.load_plugin()

    async def edit_or_reply(self, message: Message, text: str) -> Message:
        if message.from_user and message.from_user.id in Config.SUDO_USERS:
            if message.reply_to_message:
                return await message.reply_to_message.reply_text(text)
            return await message.reply_text(text)
        return await message.edit_text(text)

    async def log(self, tag: str, text: str, file: str = None) -> None:
        msg = f"**#{tag.upper()}**\n\n{text}"
        try:
            if file:
                await self.bot.send_document(Config.LOGGER_ID, file, caption=msg)
            else:
                await self.bot.send_message(
                    Config.LOGGER_ID, msg, disable_web_page_preview=True
                )
        except Exception as e:
            raise Exception(f"{Symbols.cross_mark} LogErr: {e}")


hellbot = HellClient()
