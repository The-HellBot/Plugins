from Hellbot.core import db


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


Flood = AntiFlood()
