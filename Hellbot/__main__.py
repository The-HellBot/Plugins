from pyrogram import idle

from Hellbot.core import UserSetup, db, hellbot
from Hellbot.functions.utility import BList, Flood, TGraph


async def main():
    await hellbot.startup()
    await db.connect()
    await UserSetup()
    await Flood.updateFromDB()
    await BList.updateBlacklists()
    await TGraph.setup()
    await hellbot.start_message()
    await idle()


if __name__ == "__main__":
    hellbot.run(main())
