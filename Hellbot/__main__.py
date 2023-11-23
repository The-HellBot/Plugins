from pyrogram import idle

from Hellbot.core import Users, db, hellbot
from Hellbot.functions.setup import Flood, BList


async def main():
    await hellbot.startup()
    await db.connect()
    await Users().setup()
    await Flood.updateFromDB()
    await BList.updateBlacklists()
    await idle()


if __name__ == "__main__":
    hellbot.run(main())
