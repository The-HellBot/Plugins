from pyrogram import idle

from Hellbot.core import Users, db, hellbot
from Hellbot.functions.utility import BList, Flood, TGraph


async def main():
    await hellbot.startup()
    await db.connect()
    await Users().setup()
    await Flood.updateFromDB()
    await BList.updateBlacklists()
    await TGraph.setup()
    await hellbot.start_message()
    await idle()


if __name__ == "__main__":
    hellbot.run(main())
