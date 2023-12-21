import asyncio
import os

import heroku3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
from pyrogram.types import Message

from Hellbot import HEROKU_APP
from Hellbot.core import LOGS
from Hellbot.functions.tools import gen_changelogs, restart, runcmd

from . import Config, HelpMenu, hellbot, on_message


@on_message("restart", allow_stan=True)
async def restart_bot(_, message: Message):
    try:
        await hellbot.edit(message, "💫 Restarted Bot Successfully!")
        await restart()
    except Exception as e:
        LOGS.error(e)


@on_message("shutdown", allow_stan=True)
async def shutdown_bot(_, message: Message):
    await hellbot.edit(
        message,
        "**[ ⚠️ ]** __HellBot is now offline! Manually start again to get it back online.__"
    )
    try:
        if HEROKU_APP:
            try:
                heroku = heroku3.from_key(Config.HEROKU_APIKEY)
                app = heroku.apps()[Config.HEROKU_APPNAME]
                app.process_formation()["worker"].scale(0)
            except BaseException as e:
                await restart(shutdown=True)
    except:
        await restart(shutdown=True)


@on_message("cleanup", allow_stan=True)
async def clenup_bot(_, message: Message):
    await hellbot.edit(message, "**♻️ HellBot Cleanup Completed!**")
    await restart(clean_up=True)


@on_message("update", allow_stan=True)
async def update_bot(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(
            message, "**[ ⚠️ ]** __Please specify what to update.__"
        )

    hell = await hellbot.edit(message, "**🔄 𝖨𝗇 𝖯𝗋𝗈𝗀𝗋𝖾𝗌𝗌...**")
    cmd = message.command[1].lower()

    if cmd == "plugins":
        if HEROKU_APP:
            try:
                heroku = heroku3.from_key(Config.HEROKU_APIKEY)
                app = heroku.apps()[Config.HEROKU_APPNAME]
                await hell.edit(
                    "**🔄 𝖴𝗉𝖽𝖺𝗍𝖾𝖽 𝖯𝗅𝗎𝗀𝗂𝗇𝗌 𝗋𝖾𝗉𝗈!** \n__𝖡𝗈𝗍 𝗐𝗂𝗅𝗅 𝗌𝗍𝖺𝗋𝗍 𝗐𝗈𝗋𝗄𝗂𝗇𝗀 𝖺𝖿𝗍𝖾𝗋 1 𝗆𝗂𝗇𝗎𝗍𝖾.__"
                )
                app.restart()
            except Exception as e:
                return await hellbot.error(message, f"`{e}`")
        else:
            await hell.edit(
                "**🔄 𝖴𝗉𝖽𝖺𝗍𝖾𝖽 𝖯𝗅𝗎𝗀𝗂𝗇𝗌 𝗋𝖾𝗉𝗈!** \n__𝖡𝗈𝗍 𝗐𝗂𝗅𝗅 𝗌𝗍𝖺𝗋𝗍 𝗐𝗈𝗋𝗄𝗂𝗇𝗀 𝖺𝖿𝗍𝖾𝗋 1 𝗆𝗂𝗇𝗎𝗍𝖾.__"
            )
            return await restart(update=True)

    elif cmd == "deploy":
        if HEROKU_APP:
            os.chdir("/app")
            try:
                repo = Repo()
            except NoSuchPathError as e:
                return await hellbot.error(hell, f"__No GitRepo found:__ `{e}`")
            except GitCommandError as e:
                return await hellbot.error(hell, f"__Invalid Git Command:__ `{e}`")
            except InvalidGitRepositoryError as e:
                return await hellbot.error(hell, f"__Invalid Git Repo.__ `{e}`")

            await runcmd(f"git fetch orgin {Config.DEPLOY_BRANCH} &> /dev/null")
            await asyncio.sleep(5)

            changelogs = await gen_changelogs(repo, Config.DEPLOY_BRANCH)
            if not changelogs:
                return await hell.edit("**🔁 𝖣𝖾𝗉𝗅𝗈𝗒 𝗂𝓈 𝓊𝓅 𝓉𝑜 𝒹𝒶𝓉𝑒!**")

            await hell.edit(
                f"**🔄 𝖣𝖾𝗉𝗅𝗈𝗒𝗂𝗇𝗀 𝖨𝗇 𝖯𝗋𝗈𝗀𝗋𝖾𝗌𝗌...**\n\n**📑 𝖢𝗁𝖺𝗇𝗀𝖾𝗅𝗈𝗀𝗌:**\n{changelogs}"
            )

            os.system("git stash &> /dev/null && git pull")
            os.system(
                f"git push https://{Config.HEROKU_APIKEY}@git.heroku.com/{Config.HEROKU_APPNAME}.git HEAD:master"
            )
        else:
            await hell.edit(
                "**🔄 𝖣𝖾𝗉𝗅𝗈𝗒𝗂𝗇𝗀 𝖨𝗇 𝖯𝗋𝗈𝗀𝗋𝖾𝗌𝗌...**\n\n__Please wait for a minute or two.__"
            )
            return await restart(update=True)
    else:
        return await hellbot.delete(
            hell, f"**[ ⚠️ ]** __Invalid update argument:__ `{cmd}`"
        )


HelpMenu("power").add(
    "restart", None, "Restart the bot. It might take 2 minutes to execute.", "restart"
).add(
    "shutdown",
    None,
    "Shutdown the bot. Will permanently turn off the bot until started manually.",
    "shutdown",
).add(
    "cleanup",
    None,
    "Cleanup the bot. Delete downloaded files and temp files.",
    "cleanup",
).add(
    "update plugins",
    None,
    "Updates the plugins to the latest code if there is any update available, else it'll just restart the bot.",
    "update plugins",
).add(
    "update deploy",
    None,
    "Updates the main code base to the latest commit.",
    "update deploy",
    "This process might take upto 5 minutes to complete.",
).info(
    "Commands to manage the bot."
).done()
