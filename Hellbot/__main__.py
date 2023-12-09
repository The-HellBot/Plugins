from pyrogram import idle

from Hellbot.core import Users, db, hellbot
from Hellbot.functions.utility import BList, Flood


async def main():
    await hellbot.startup()
    await db.connect()
    await Users().setup()
    await Flood.updateFromDB()
    await BList.updateBlacklists()
    await idle()


if __name__ == "__main__":
    hellbot.run(main())
