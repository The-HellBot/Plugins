import contextlib
import os

import heroku3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
from pyrogram.types import Message

from Hellbot import HEROKU_APP
from Hellbot.core import LOGS
from Hellbot.functions.tools import restart, gen_changelogs, initialize_git

from . import Config, HelpMenu, hellbot, on_message


@on_message("restart", allow_stan=True)
async def restart_bot(_, message: Message):
    await hellbot.edit(message, "💫 Restarted Bot Successfully!")
    try:
        if HEROKU_APP:
            try:
                heroku = heroku3.from_key(Config.HEROKU_APIKEY)
                app = heroku.apps()[Config.HEROKU_APPNAME]
                app.restart()
            except:
                await restart()
        else:
            await restart()
    except Exception as e:
        LOGS.error(e)


@on_message("shutdown", allow_stan=True)
async def shutdown_bot(_, message: Message):
    await hellbot.edit(
        message,
        "**[ ⚠️ ]** __HellBot is now offline! Manually start again to get it back online.__",
    )
    try:
        if HEROKU_APP:
            try:
                heroku = heroku3.from_key(Config.HEROKU_APIKEY)
                app = heroku.apps()[Config.HEROKU_APPNAME]
                app.process_formation()["worker"].scale(0)
            except:
                await restart(shutdown=True)
        else:
            await restart(shutdown=True)
    except Exception as e:
        LOGS.error(e)


@on_message("cleanup", allow_stan=True)
async def clenup_bot(_, message: Message):
    await hellbot.edit(message, "**♻️ HellBot Cleanup Completed!**")
    await restart(clean_up=True)


@on_message("update", allow_stan=True)
async def update_bot(_, message: Message):
    hell = await hellbot.edit(message, "**🔄 𝖨𝗇 𝖯𝗋𝗈𝗀𝗋𝖾𝗌𝗌...**")

    if len(message.command) < 2:
        status, repo, force = await initialize_git(Config.PLUGINS_REPO)
        if not status:
            return await hellbot.error(hell, repo)

        active_branch = repo.active_branch.name
        upstream = repo.remote("upstream")
        upstream.fetch(active_branch)

        changelogs = await gen_changelogs(repo, f"HEAD..upstream/{active_branch}")
        if not changelogs and not force:
            repo.__del__()
            return await hellbot.delete(
                hell, "__There are no updates available right now.__"
            )

        if force:
            return await hell.edit(
                f"Force-Sync in progress... Please wait for a moment and try again.\n\n{changelogs}",
                disable_web_page_preview=True,
            )

        return await hell.edit(
            f"**🍂 𝖴𝗉𝖽𝖺𝗍𝖾 𝖠𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 𝖿𝗈𝗋 𝖯𝗅𝗎𝗀𝗂𝗇𝗌:**\n\n{changelogs}",
            disable_web_page_preview=True,
        )

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
            status, repo, _ = await initialize_git(Config.DEPLOY_REPO)
            if not status:
                return await hellbot.error(hell, repo)

            active_branch = repo.active_branch.name
            upstream = repo.remote("upstream")
            upstream.fetch(active_branch)

            heroku = heroku3.from_key(Config.HEROKU_APIKEY)
            app = heroku.apps()[Config.HEROKU_APPNAME]

            await hell.edit(
                "**🔄 𝖣𝖾𝗉𝗅𝗈𝗒𝗂𝗇𝗀 𝖨𝗇 𝖯𝗋𝗈𝗀𝗋𝖾𝗌𝗌...**\nThis might take upto 5 minutes to complete!"
            )
            repo.git.reset("--hard", "FETCH_HEAD")
            heroku_git = app.git_url.replace(
                "https://", f"https://api:{Config.HEROKU_APIKEY}@"
            )

            if "heroku" in repo.remotes:
                remote = repo.remote("heroku")
                remote.set_url(heroku_git)
            else:
                remote = repo.create_remote("heroku", heroku_git)

            try:
                remote.push(f"HEAD:refs/heads/master", force=True)
            except BaseException as e:
                repo.__del__()
                return await hellbot.error(hell, f"__Invalid Heroku Creds:__ `{e}`")

            build = app.builds(order_by="created_at", sort="desc")[0]
            if build.status == "failed":
                return await hellbot.error(
                    hell,
                    "__There were some problems with the update! Make sure your heroku api and app name are correct.__",
                )

            try:
                remote.push("master:main", force=True)
            except BaseException as e:
                repo.__del__()
                return await hellbot.error(hell, f"__Invalid Heroku Creds:__ `{e}`")
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
    "update",
    None,
    "Check if there's any update available for the bot. If there is, it'll give new last 5 changelogs.",
    "update",
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
