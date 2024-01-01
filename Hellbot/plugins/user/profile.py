import datetime
import os

import requests
from pyrogram import Client
from pyrogram.types import InputMediaPhoto, Message

from Hellbot.functions.templates import github_user_templates

from . import Config, HelpMenu, hellbot, on_message


@on_message("getpfp", allow_stan=True)
async def getpfp(client: Client, message: Message):
    hell = await hellbot.edit(message, "Processing...")
    limit = 1

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        reply_to = message.reply_to_message.id

        if len(message.command) >= 2:
            if message.command[1].isdigit():
                limit = int(message.command[1])
            elif message.command[1] == "all":
                limit = 0

    elif len(message.command) >= 2:
        try:
            user = await client.get_users(message.command[1])
            reply_to = message.id

            if len(message.command) > 2:
                if message.command[2].isdigit():
                    limit = int(message.command[2])
                elif message.command[2] == "all":
                    limit = 0

        except Exception as e:
            return await hellbot.error(hell, f"`{str(e)}`")

    else:
        return await hellbot.delete(
            hell, f"Reply to a message or pass a username/id to get the profile pic."
        )

    if not user.photo:
        return await hellbot.error(hell, f"User {user.mention} has no profile pic.")

    if limit == 1:
        async for photo in client.get_chat_photos(user.id, 1):
            await client.send_photo(
                message.chat.id,
                photo.file_id,
                f"**Profile Pic of User** {user.mention}",
                reply_to_message_id=reply_to,
            )
    else:
        profile_pics = []
        async for photo in client.get_chat_photos(user.id, limit):
            profile_pics.append(InputMediaPhoto(photo.file_id))

        await client.send_media_group(
            message.chat.id,
            profile_pics,
            reply_to_message_id=reply_to,
        )

    await hell.delete()


@on_message("setpfp", allow_stan=True)
async def setpfp(client: Client, message: Message):
    if not message.reply_to_message:
        return await hellbot.delete(message, "Reply to a photo to set as profile pic.")

    hell = await hellbot.edit(message, "Processing...")

    try:
        if message.reply_to_message.photo:
            dwl_path = await message.reply_to_message.download(Config.DWL_DIR)
            await client.set_profile_photo(photo=dwl_path)
        elif message.reply_to_message.video:
            dwl_path = await message.reply_to_message.download(Config.DWL_DIR)
            await client.set_profile_photo(video=dwl_path)
        else:
            return await hellbot.delete(
                hell, "Reply to a photo or video to set as profile pic."
            )
    except Exception as e:
        return await hellbot.error(hell, f"`{str(e)}`")

    await hellbot.delete(hell, "Profile pic updated successfully.")
    await hellbot.check_and_log(
        "setpfp",
        f"**User:** {message.from_user.mention} (`{message.from_user.id}`)",
        dwl_path,
    )

    os.remove(dwl_path)


@on_message("setbio", allow_stan=True)
async def setbio(client: Client, message: Message):
    bio = await hellbot.input(message)
    hell = await hellbot.edit(message, "Processing...")

    try:
        await client.update_profile(bio=bio)
    except Exception as e:
        return await hellbot.error(hell, f"`{str(e)}`")

    await hellbot.delete(hell, "Bio updated successfully.")
    await hellbot.check_and_log(
        "setbio",
        f"**User:** {message.from_user.mention} (`{message.from_user.id}`)\n\n**Bio:** `{bio}`",
    )


@on_message("setname", allow_stan=True)
async def setname(client: Client, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(message, "Pass a name to set.")

    name = await hellbot.input(message)
    hell = await hellbot.edit(message, "Processing...")

    try:
        await client.update_profile(first_name=name)
    except Exception as e:
        return await hellbot.error(hell, f"`{str(e)}`")

    await hellbot.delete(hell, "Name updated successfully.")
    await hellbot.check_and_log(
        "setname",
        f"**User:** {message.from_user.mention} (`{message.from_user.id}`)\n\n**Name:** `{name}`",
    )


@on_message("setusername", allow_stan=True)
async def setusername(client: Client, message: Message):
    username = message.command[1] if len(message.command) > 1 else None
    hell = await hellbot.edit(message, "Processing...")

    try:
        await client.set_username(username)
    except Exception as e:
        return await hellbot.error(hell, f"`{str(e)}`")

    await hellbot.delete(hell, "Username updated successfully.")
    await hellbot.check_and_log(
        "setusername",
        f"**User:** {message.from_user.mention} (`{message.from_user.id}`)\n\n**Username:** `{username}`",
    )


@on_message("delpfp", allow_stan=True)
async def delpfp(client: Client, message: Message):
    limit = (
        1
        if len(message.command) < 2
        else int(message.command[1])
        if message.command[1].isdigit()
        else 1
    )

    hell = await hellbot.edit(message, "Processing...")
    profile_pics = []

    async for photo in client.get_chat_photos(client.me.id, limit):
        profile_pics.append(photo.file_id)

    if not profile_pics:
        return await hellbot.error(hell, "No profile pics found.")

    await client.delete_profile_photos(profile_pics)


@on_message("github", allow_stan=True)
async def gituser(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(message, "Pass a github username to search.")

    hell = await hellbot.edit(message, "Processing...")
    username = message.command[1]

    try:
        response = requests.get(f"https://api.github.com/users/{username}").json()
        avatar_url = response["avatar_url"]
        bio = response["bio"]
        blog = response["blog"]
        company = response["company"]
        created_at = datetime.datetime.strptime(
            response["created_at"], "%Y-%m-%dT%H:%M:%SZ"
        )
        email = response["email"]
        followers = response["followers"]
        following = response["following"]
        git_id = response["id"]
        id_type = response["type"]
        location = response["location"]
        name = response["name"]
        profile_url = response["html_url"]
        public_gists = response["public_gists"]
        public_repos = response["public_repos"]
        username = response["login"]
        if not bio:
            bio = "No bio found."

        file = f"{Config.TEMP_DIR}{username}.jpg"
        resp = requests.get(avatar_url)
        with open(file, "wb") as f:
            f.write(resp.content)

        await message.reply_photo(
            file,
            caption=await github_user_templates(
                username=username,
                git_id=git_id,
                id_type=id_type,
                name=name,
                profile_url=profile_url,
                blog=blog,
                company=company,
                email=email,
                location=location,
                public_repos=public_repos,
                public_gists=public_gists,
                followers=followers,
                following=following,
                created_at=created_at.strftime("%d %B %Y"),
                bio=bio,
            ),
        )
        await hell.delete()
        os.remove(file)
    except Exception as e:
        return await hellbot.error(hell, f"`{str(e)}`")


HelpMenu("profile").add(
    "getpfp",
    "<reply/username/id> <limit>",
    "Get number of profile pic of a user.",
    "getpfp @ForGo10God 5",
).add(
    "setpfp",
    "<reply to photo>",
    "Set the profile picture of your telegram account.",
    "setpfp",
).add(
    "setbio",
    "<new bio>",
    "Set the bio of the bot.",
    "setbio Embracing the Hellbot.",
    "To remove the bio dont pass any argument.",
).add(
    "setname", "<new name>", "Set the name of the bot.", "setname HellBot"
).add(
    "setusername",
    "<new username>",
    "Set the username of the bot.",
    "setusername HellBot",
    "To remove the username dont pass any argument.",
).add(
    "delpfp",
    "<limit>",
    "Delete the profile pics of the bot.",
    "delpfp 5",
    "To delete all profile pics pass 0 as limit.",
).add(
    "github",
    "<username>",
    "Get the github profile of a user.",
    "github hellboy-op",
).info(
    "Profile Module"
).done()
