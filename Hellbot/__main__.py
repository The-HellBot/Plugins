from pyrogram import idle

from Hellbot.core import UserSetup, db, hellbot
from Hellbot.functions.utility import BList, Flood, TGraph
from Hellbot import __version__


async def main():
    await hellbot.startup()
    await db.connect()
    await UserSetup()
    await Flood.updateFromDB()
    await BList.updateBlacklists()
    await TGraph.setup()
    await hellbot.start_message(__version__)
    await idle()


if __name__ == "__main__":
    hellbot.run(main())
