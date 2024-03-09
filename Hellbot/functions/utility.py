import asyncio
import os
import time

from pyrogram import Client
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from telegraph import Telegraph

from Hellbot.core import ENV, db

from .formatter import readable_time


class TelegraphAPI:
    def __init__(self) -> None:
        self.shortname: str = "TheHellbot"
        self.telegraph: Telegraph = None

    async def setup(self):
        shortname = await db.get_env(ENV.telegraph_account) or self.shortname

        self.telegraph = Telegraph()
        self.telegraph.create_account(shortname)


class Gcast:
    def __init__(self) -> None:
        self.file_name = "gcast_{0}.txt"
        self.complete_msg = "**🍀 𝖦𝖼𝖺𝗌𝗍 𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽!** \n\n**𝖬𝖾𝗌𝗌𝖺𝗀𝖾:** [click here]({0})\n**𝖢𝗈𝗎𝗇𝗍:** `{1} {2}`\n**𝖥𝗈𝗋𝗐𝖺𝗋𝖽 𝗍𝖺𝗀:** `{3}`\n**𝖳𝗂𝗆𝖾 𝗍𝖺𝗄𝖾𝗇:** `{4}`"

    async def _send_msg(self, chat_id: int, msg: Message, tag: bool):
        await msg.forward(chat_id) if tag else await msg.copy(chat_id)

    async def start(self, message: Message, client: Client, mode: str, tag: bool):
        link = message.link
        status = "Enabled" if tag else "Removed"
        start = time.time()

        if mode == "all":
            uCount, uFileName = await self.users(message, client, tag)
            gCount, gFileName = await self.groups(message, client, tag)
            count = uCount + gCount
            with open(uFileName, "a", encoding="utf-8") as file1, open(
                gFileName, "r", encoding="utf-8"
            ) as file2:
                file1.write(file2.read())
            file2.close()
            file1.close()
            os.remove(gFileName)
            fileName = uFileName
        elif mode == "groups":
            count, fileName = await self.groups(message, client, tag)
        elif mode == "users":
            count, fileName = await self.users(message, client, tag)
        else:
            return None

        end = time.time()
        outStr = self.complete_msg.format(
            link, count, mode, status, readable_time(int(end - start))
        )

        return fileName, outStr

    async def groups(self, message: Message, client: Client, tag: bool):
        filename = self.file_name.format(round(time.time()))
        count = 0

        with open(filename, "w", encoding="utf-8") as f:
            f.write("Group ID | Error\n\n")
            async for dialog in client.get_dialogs():
                if dialog.chat.type == ChatType.SUPERGROUP:
                    try:
                        await self._send_msg(dialog.chat.id, message, tag)
                        count += 1
                    except FloodWait as fw:
                        await asyncio.sleep(fw.value)
                        await self._send_msg(dialog.chat.id, message, tag)
                        count += 1
                    except Exception as e:
                        f.write(f"{dialog.chat.id} | {e}\n")

        f.close()

        return count, filename

    async def users(self, message: Message, client: Client, tag: bool):
        filename = self.file_name.format(round(time.time()))
        count = 0

        with open(filename, "w", encoding="utf-8") as f:
            f.write("User ID | Error\n\n")
            async for dialog in client.get_dialogs():
                if dialog.chat.type == ChatType.PRIVATE:
                    try:
                        await self._send_msg(dialog.chat.id, message, tag)
                        count += 1
                    except FloodWait as fw:
                        await asyncio.sleep(fw.value)
                        await self._send_msg(dialog.chat.id, message, tag)
                        count += 1
                    except Exception as e:
                        f.write(f"{dialog.chat.id} | {e}\n")

        f.close()

        return count, filename


class AntiFlood:
    def __init__(self) -> None:
        self.FloodCount = {}
        self.settings = {}
        self.client_chats = {}

    def updateSettings(self, client: int, chat: int, data: dict):
        mode = data.get("mode", "mute")
        mtime = data.get("time", 0)
        limit = data.get("limit", 5)

        self.settings[client] = {chat: {"mode": mode, "time": mtime, "limit": limit}}

    def getSettings(self, client: int, chat: int) -> tuple[str, int, int]:
        mode = "mute"
        mtime = 0
        limit = 5

        cli_settings: dict = self.settings.get(client, None)
        if cli_settings:
            chat_settings: dict = cli_settings.get(chat, None)
            if chat_settings:
                mode = chat_settings.get("mode", "mute")
                mtime = chat_settings.get("time", 0)
                limit = chat_settings.get("limit", 5)

        return mode, int(mtime), limit

    def updateFlood(self, client: int, chat: int, user: int, count: int):
        self.FloodCount[client] = {chat: {"last_user": user, "count": count}}

    def getLastUser(self, client: int, chat: int) -> tuple[int, int]:
        try:
            cli_dict: dict = self.FloodCount[client]
        except KeyError:
            self.FloodCount[client] = {}
            cli_dict: dict = self.FloodCount[client]

        try:
            chat_dict: dict = cli_dict[chat]
        except KeyError:
            cli_dict[chat] = {}
            chat_dict: dict = cli_dict[chat]

        last_user: int = chat_dict.get("last_user", 0)
        count: int = chat_dict.get("count", 0)

        return last_user, count

    async def updateFromDB(self):
        floods = await db.get_all_floods()
        for flood in floods:
            client = flood["client"]
            chat = flood["chat"]
            mode = flood.get("mode", "mute")
            mtime = flood.get("time", 0)
            limit = flood.get("limit", 5)
            settings = {"mode": mode, "time": mtime, "limit": limit}

            self.updateSettings(client, chat, settings)
            try:
                self.client_chats[client].append(chat)
            except KeyError:
                self.client_chats[client] = [chat]

    def check_client_chat(self, client: int, chat: int) -> bool:
        try:
            chats = self.client_chats[client]
        except KeyError:
            return False

        if chat in chats:
            return True

        return False


class Blacklists:
    def __init__(self) -> None:
        self.blacklists = {}

    async def updateBlacklists(self):
        datas = await db.get_blacklist_clients()
        for data in datas:
            client = data["client"]
            chats = data.get("chats", [])
            for chat in chats:
                blacklists = data["blacklist"]
                self.blacklists[client] = {chat: blacklists}

    async def addBlacklist(self, client: int, chat: int, text: str):
        try:
            self.blacklists[client][chat].append(text)
        except KeyError:
            self.blacklists[client] = {chat: [text]}

        await db.add_blacklist(client, chat, text)

    async def rmBlacklist(self, client: int, chat: int, text: str):
        try:
            self.blacklists[client][chat].remove(text)
        except KeyError:
            return

        await db.rm_blacklist(client, chat, text)

    def getBlacklists(self, client: int, chat: int) -> list:
        try:
            return self.blacklists[client][chat]
        except KeyError:
            return []

    def check_client_chat(self, client: int, chat: int) -> bool:
        try:
            chats = self.blacklists[client]
        except KeyError:
            return False

        if chat in chats:
            return True

        return False


Flood = AntiFlood()
BList = Blacklists()
TGraph = TelegraphAPI()
