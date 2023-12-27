from pyrogram import idle

from Hellbot import __version__
from Hellbot.core import ForcesubSetup, UserSetup, db, hellbot
from Hellbot.functions.utility import BList, Flood, TGraph


async def main():
    await hellbot.startup()
    await db.connect()
    await UserSetup()
    await ForcesubSetup()
    await Flood.updateFromDB()
    await BList.updateBlacklists()
    await TGraph.setup()
    await hellbot.start_message(__version__)
    await idle()


if __name__ == "__main__":
    hellbot.run(main())
