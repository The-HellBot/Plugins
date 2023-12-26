import os
import re
import time

import requests
from pyrogram.types import Message
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

from Hellbot.functions.driver import Driver

from . import HelpMenu, hellbot, on_message

@on_message("reels", allow_stan=True)
async def instagramReels(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(
            message, "Give an instagram reels link to download."
        )

    hell = await hellbot.edit(message, "Searching...")

    query = await hellbot.input(message)
    isInstagramLink = lambda link: bool(
        (re.compile(r"^https?://(?:www\.)?instagram\.com/reel/")).match(link)
    )

    if not isInstagramLink(query):
        return await hellbot.error(hell, "Give a valid instagram reels link.")

    try:
        driver, _ = Driver.get()
        if not driver:
            return await hellbot.error(hell, _)

        driver.get(query)
        wait = WebDriverWait(driver, 10)
        element = wait.until(presence_of_element_located((By.TAG_NAME, "video")))
        reels = element.get_attribute("src")
        driver.quit()

        if reels:
            await hell.edit("Found the reel. **Downloading...**")

            binary = requests.get(reels).content
            fileName = f"reels_{int(time.time())}.mp4"
            with open(fileName, "wb") as file:
                file.write(binary)

            await hell.edit("Uploading...")
            await message.reply_video(
                fileName,
                caption=f"__💫 Downloaded Instagram Reels!__ \n\n**</> @HellBot_Networks**",
            )
            await hell.delete()
            os.remove(fileName)
        else:
            await hellbot.error(
                hell,
                "Unable to download the reel. Make sure the link is valid or the reel is not from a private account.",
            )
    except Exception as e:
        await hellbot.error(hell, f"**Error:** `{e}`")


@on_message("igpost", allow_stan=True)
async def instagramPost(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(message, "Give an instagram post link to download.")

    hell = await hellbot.edit(message, "Searching...")

    query = await hellbot.input(message)
    isInstagramLink = lambda link: bool(
        (re.compile(r"^https?://(?:www\.)?instagram\.com/p/")).match(link)
    )

    if not isInstagramLink(query):
        return await hellbot.error(hell, "Give a valid instagram post link.")

    try:
        driver, _ = Driver.get()
        if not driver:
            return await hellbot.error(hell, _)

        reels = []
        driver.get(query)
        wait = WebDriverWait(driver, 10)
        element = wait.until(presence_of_element_located((By.TAG_NAME, "video")))
        reels.append(element.get_attribute("src"))

        for _ in range(10):
            try:
                driver.find_element(By.XPATH, "//button[@aria-label='Next']").click()
                element = wait.until(presence_of_element_located((By.TAG_NAME, "video")))
                reels.append(element.get_attribute("src"))
            except:
                break

        driver.quit()

        if reels:
            await hell.edit("**Downloading...**")

            for reel in reels:
                binary = requests.get(reel).content
                fileName = f"post_{int(time.time())}.mp4"
                with open(fileName, "wb") as file:
                    file.write(binary)
                await message.reply_video(
                    fileName,
                    caption=f"__💫 Downloaded Instagram Post!__ \n\n**</> @HellBot_Networks**",
                )
                await hell.delete()
                os.remove(fileName)
        else:
            await hellbot.error(
                hell,
                "Unable to download the post. Make sure the link is valid or the post is not from a private account.",
            )
    except Exception as e:
        await hellbot.error(hell, f"`{e}`")


@on_message("iguser", allow_stan=True)
async def instagramUser(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(message, "Give an instagram username to fetch info.")


    query = await hellbot.input(message)
    query = query.replace("@", "").strip()

    hell = await hellbot.edit(message, f"**Searching** `{query}` **on instagram**...")
    url = f"https://instagram.com/{query}/"

    driver, _ = Driver.get()
    if not driver:
        return await hellbot.error(hell, f"**Unable to get driver:** `{_}`")

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        element = wait.until(presence_of_element_located((By.XPATH, "//img[@alt='Profile photo']")))
        profilePic = element.get_attribute("src")
        about = driver.find_element(By.XPATH, "//div/h1").text

        profile_info_ul = driver.find_elements(By.XPATH, "//ul[@class='x78zum5 x1q0g3np xieb3on']/li/button")  # post, followers, following
        posts = profile_info_ul[0].text
        followers = profile_info_ul[1].text
        following = profile_info_ul[2].text

        fileName = f"iguser_{int(time.time())}.jpg"
        binary = requests.get(profilePic).content
        with open(fileName, "wb") as file:
            file.write(binary)

        await message.reply_photo(
            fileName,
            caption=f"**💬 𝖠𝖻𝗈𝗎𝗍:** `{about}`\n\n**📸 𝖯𝗈𝗌𝗍𝗌:** `{posts}`\n**💫 𝖥𝗈𝗅𝗅𝗈𝗐𝖾𝗋𝗌:** `{followers}`\n**🍀 𝖥𝗈𝗅𝗅𝗈𝗐𝗂𝗇𝗀:** `{following}`\n\n**</> @HellBot_Networks**",
        )
        await hell.delete()
        os.remove(fileName)
    except Exception as e:
        return await hellbot.error(hell, f"`{e}`")


HelpMenu("instagram").add(
    "reels",
    "<instagram reels link>",
    "Download instagram reels.",
    "reels https://www.instagram.com/reel/Cr24EiKNTL7/",
).add(
    "igpost",
    "<instagram post link>",
    "Download instagram post.",
    "igpost https://www.instagram.com/p/C06rAjDJlJs/",
    "If the post has multiple videos, it will download all of them one by one.",
).add(
    "iguser", #Bugged: to-be-fixed
    "<instagram username>",
    "Get instagram user info.",
    "iguser therock",
).info(
    "Instagram Scrapper"
).done()
