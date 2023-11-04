from Hellbot.core.config import Config, Symbols


class HelpMenu:
    def __init__(self, file: str) -> None:
        self.filename = file
        self.command_dict = {}
        self.command_info = ""

    def add(
        self,
        command: str,
        parameters: str = None,
        description: str = None,
        example: str = None,
        note: str = None,
    ):
        self.command_dict[command] = {
            "command": command,
            "parameters": parameters,
            "description": description,
            "example": example,
            "note": note,
        }
        return self

    def info(self, command_info: str):
        self.command_info = command_info
        return self

    def get_menu(self) -> str:
        result = f"**𝖯𝗅𝗎𝗀𝗂𝗇 𝖥𝗂𝗅𝖾:** `{self.filename}`"
        if self.command_info:
            result += f"\n**𝖯𝗅𝗎𝗀𝗂𝗇 𝖨𝗇𝖿𝗈:** __{self.command_info} 🍀__"
        result += "\n\n"
        for command in self.command_dict:
            command = self.command_dict[command]
            result += f"**{Symbols.radio_select} 𝖢𝗈𝗆𝗆𝖺𝗇𝖽:** `{Config.HANDLERS[0]}{command['command']}"
            if command["parameters"]:
                result += f" {command['parameters']}`\n"
            else:
                result += "`\n"
            if command["description"]:
                result += (
                    f"**{Symbols.arrow_right} 𝖣𝖾𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇:** __{command['description']}__\n"
                )
            if command["example"]:
                result += f"**{Symbols.arrow_right} 𝖤𝗑𝖺𝗆𝗉𝗅𝖾:** `{Config.HANDLERS[0]}{command['example']}`\n"
            if command["note"]:
                result += f"**{Symbols.arrow_right} 𝖭𝗈𝗍𝖾:** __{command['note']}__\n"

            result += f"\n**<\> @Its_HellBot 🍀**"

            Config.CMD_INFO[command["command"]] = {
                "command": f"{command['command']} {command['parameters'] if command['parameters'] else ''}",
                "description": command["description"],
                "example": command["example"],
                "note": command["note"],
                "plugin": self.filename,
            }

        return result

    def done(self) -> None:
        Config.HELP_DICT[self.filename] = {
            "commands": self.command_dict,
            "info": self.command_info,
        }
        Config.CMD_MENU[self.filename] = self.get_menu()


class BotHelp:
    def __init__(self, file: str) -> None:
        self.category = file
        self.command_dict = {}
        self.command_info = ""

    def add(self, command: str, description: str):
        self.command_dict[command] = {"command": command, "description": description}
        return self

    def info(self, command_info: str):
        self.command_info = command_info
        return self

    def get_menu(self) -> str:
        result = f"**𝖯𝗅𝗎𝗀𝗂𝗇 𝖢𝖺𝗍𝖾𝗀𝗈𝗋𝗒:** `{self.category}`"
        if self.command_info:
            result += f"\n**𝖯𝗅𝗎𝗀𝗂𝗇 𝖨𝗇𝖿𝗈:** __{self.command_info}__"
        result += "\n\n"
        for command in self.command_dict:
            command = self.command_dict[command]
            result += f"**{Symbols.radio_select} 𝖢𝗈𝗆𝗆𝖺𝗇𝖽:** `/{command['command']}`\n"
            if command["description"]:
                result += (
                    f"**{Symbols.arrow_right} 𝖣𝖾𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇:** __{command['description']}__\n"
                )
            result += "\n"

            Config.BOT_CMD_INFO[command["command"]] = {
                "command": command["command"],
                "description": command["description"],
                "category": self.category,
            }

        return result

    def done(self) -> None:
        Config.BOT_HELP[self.category] = {
            "commands": self.command_dict,
            "info": self.command_info,
        }
        Config.BOT_CMD_MENU[self.category] = self.get_menu()


# example usage of HelpMenu class
"""
HelpMenu("example").add(
    "example", "<text>", "description of command", "example of command", "note of command"
).info(
    "information of plugin"
).done()
"""

# example usage of BotHelp class
"""
BotHelp("example").add(
    "example", "description of command"
).info(
    "information of category"
).done()
"""
