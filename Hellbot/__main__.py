import pyroaddon
from pyrogram import idle

from Hellbot.core import Users, db, hellbot


async def main():
    await hellbot.startup()
    await db.connect()
    await Users().setup()
    await idle()


if __name__ == "__main__":
    hellbot.run(main())
