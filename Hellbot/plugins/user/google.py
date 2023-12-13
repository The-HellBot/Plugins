import io
import os
import urllib.request
from shutil import rmtree

import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from geopy.location import Location
from googlesearch import search
from pyrogram import Client
from pyrogram.types import InputMediaPhoto, Message
from wikipedia import exceptions, summary

from Hellbot.functions.driver import Driver
from Hellbot.functions.google import googleimagesdownload
from Hellbot.functions.scraping import is_valid_url

from . import Config, HelpMenu, Symbols, db, hellbot, on_message


@on_message("wikipedia", allow_stan=True)
async def google_search(client: Client, message: Message):
    if len(message.command) < 2:
        return await hellbot.edit(message, "Give some text to search on wikipedia.")

    search_query = await hellbot.input(message)
    hell = await hellbot.edit(
        message, f"Searching for `{search_query}` on wikipedia..."
    )

    try:
        data = summary(search_query, auto_suggest=False)
    except exceptions.DisambiguationError as error:
        error = str(error).split("\n")
        result = "".join(
            f"`{i}`\n" if lineno > 1 else f"**{i}**\n"
            for lineno, i in enumerate(error, start=1)
        )
        return await hell.edit(f"**DisambiguationError:**\n\n{result}")
    except exceptions.PageError:
        return await hellbot.delete(hell, "**Page not found.**")

    await hell.edit(
        f"**𝖲𝖾𝖺𝗋𝖼𝗁:** `{search_query}`\n**𝖱𝖾𝗌𝗎𝗅𝗍:**\n{data}",
        disable_web_page_preview=True,
    )


@on_message("google", allow_stan=True)
async def googleSearch(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.edit(message, "Give some text to search on google.")

    search_query = await hellbot.input(message)
    hell = await hellbot.edit(message, f"Searching for `{search_query}` on google...")

    try:
        results = search(search_query, 5, advanced=True)
    except Exception as error:
        return await hellbot.error(hell, f"`{str(error)}`")

    outStr = f"**🔍 𝖲𝖾𝖺𝗋𝖼𝗁:** `{search_query}`\n\n"
    for result in results:
        outStr += f"**🌐 𝖱𝖾𝗌𝗎𝗅𝗍:** [{result.title}]({result.url})\n"
        outStr += f"**📖 𝖣𝖾𝗌𝖼:** {str(result.description)[:40]}...\n\n"

    await hell.edit(outStr, disable_web_page_preview=True)


@on_message("reverse", allow_stan=True)
async def reverseSearch(_, message: Message):
    if not message.reply_to_message:
        return await hellbot.edit(
            message, "Reply to an image/sticker to reverse search it."
        )

    hell = await hellbot.edit(message, "Processing...")
    if message.reply_to_message.sticker or message.reply_to_message.photo:
        dl_path = await message.reply_to_message.download(
            Config.DWL_DIR + "reverse.jpg"
        )
        file = {"encoded_image": (dl_path, open(dl_path, "rb"))}
    else:
        return await hellbot.error(
            hell, "Reply to an image/sticker to reverse search it."
        )

    await hell.edit("Searching on google...")

    resp = requests.post(
        "https://www.google.com/searchbyimage/upload", files=file, allow_redirects=False
    )

    webresp = requests.get(
        resp.headers.get("Location"),
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0",
        },
    )

    soup = BeautifulSoup(webresp.text, "html.parser")
    div = soup.find_all("div", {"class": "r5a77d"})[0]
    alls = div.find("a")
    link = alls["href"]
    text = alls.text

    await hell.edit(
        f"**𝖯𝗈𝗌𝗌𝗂𝖻𝗅𝖾 𝖱𝖾𝗌𝗎𝗅𝗍:** [{text}]({link})", disable_web_page_preview=True
    )
    os.remove(dl_path)

    googleImage = googleimagesdownload()
    to_send = []
    args = {
        "keywords": text,
        "limit": 3,
        "format": "jpg",
        "output_directory": Config.DWL_DIR,
    }

    path_args, _ = googleImage.download(args)
    images = path_args.get(text)
    for image in images:
        to_send.append(InputMediaPhoto(image))

    if to_send:
        await hell.reply_media_group(to_send)

    try:
        rmtree(Config.DWL_DIR + text + "/")
    except:
        pass


@on_message("gps", allow_stan=True)
async def gpsLocation(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.edit(message, "Give some place name to search.")

    search_query = await hellbot.input(message)
    hell = await hellbot.edit(
        message, f"Searching for `{search_query}` on google maps..."
    )

    geolocator = Nominatim(user_agent="Hellbot")
    location: Location = geolocator.geocode(search_query)

    if not location:
        return await hellbot.delete(hell, "Location not found.")

    latitiude = location.latitude
    longitude = location.longitude
    address = location.address

    await hell.reply_location(latitiude, longitude)
    await hellbot.delete(hell, f"**🌐 𝖯𝗅𝖺𝖼𝖾:** {address}")


@on_message("webshot", allow_stan=True)
async def webScreenshot(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.edit(message, "Give some url to take screenshot.")

    search_query = await hellbot.input(message)
    if not is_valid_url(search_query):
        return await hellbot.edit(message, "Invalid url.")

    hell = await hellbot.edit(message, f"Taking screenshot of `{search_query}`...")
    driver, resp = Driver.get()
    if not driver:
        return await hellbot.error(hell, resp)

    driver.get(search_query)
    height = driver.execute_script(
        "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);"
    )
    width = driver.execute_script(
        "return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);"
    )

    driver.set_window_size(width + 100, height + 100)
    image = driver.get_screenshot_as_png()
    Driver.close(driver)

    with io.BytesIO(image) as result:
        result.name = "Hellbot_Webshot.png"
        await hell.reply_document(result)
        await hell.delete()

    try:
        os.remove("Hellbot_Webshot.png")
    except:
        pass


@on_message("cricket", allow_stan=True)
async def cricketScore(_, message: Message):
    BASE = "http://static.cricinfo.com/rss/livescores.xml"

    page = urllib.request.urlopen(BASE)
    soup = BeautifulSoup(page, "html.parser")
    result = soup.find_all("description")

    final = "**Cricket Live Score:\n\n**"
    for match in result:
        final += f"{Symbols.bullet} `{match.text}`\n"

    await hellbot.edit(message, final)


@on_message(["dictionary", "meaning", "ub"], allow_stan=True)
async def wordMeaning(_, message: Message):
    BASE = "https://api.dictionaryapi.dev/api/v2/entries/en/{0}"
    if len(message.command) < 2:
        return await hellbot.edit(message, "Give some word to search.")

    search_query = await hellbot.input(message)
    hell = await hellbot.edit(message, f"Searching for `{search_query}`...")

    response = requests.get(BASE.format(search_query))
    if response.status_code == 404:
        return await hellbot.delete(hell, "Word not found.")

    data: dict = response.json()[0]

    outStr = ""
    outStr += f"**📖W:ord** `{data.get('word', search_query)}`\n"
    outStr += f"**🔊 Phonetic:** `{data.get('phonetic', 'Not Found')}`\n"

    for meaning in data.get("meanings", []):
        outStr += f"\n**{Symbols.bullet} Part of Speech:** `{meaning.get('partOfSpeech', 'Not Found').title()}`\n"
        for definition in meaning.get("definitions", []):
            outStr += f"    {Symbols.check_mark} `{definition.get('definition', 'Not Found')}`\n"
        synonyms = meaning.get("synonyms", [])
        outStr += "**👍 Synonyms:** " + ", ".join(synonyms) if synonyms else "Not Found"
        outStr += "\n"
        antonyms = meaning.get("antonyms", [])
        outStr += "**👎 Antonyms:** " + ", ".join(antonyms) if antonyms else "Not Found"
        outStr += "\n"

    audio = data.get("phonetics", [])[0].get("audio", "")
    if audio:
        await hell.reply_audio(audio, caption=outStr)
        await hell.delete()
    else:
        await hell.edit(outStr)
