import calendar
import time

import httpx
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse
from Hellbot.core import Symbols

from .paste import post_to_telegraph
from .templates import (
    airing_templates,
    anilist_user_templates,
    anime_template,
    character_templates,
    manga_templates,
)

anime_query = """query ($id: Int,$search: String) {
    Page (perPage: 10) {
        media (id: $id, type: ANIME,search: $search) {
            id
            title {
                romaji
                english
                native
            }
            type
            format
            status
            description (asHtml: false)
            episodes
            duration
            countryOfOrigin
            source
            trailer{
                id
                site
            }
            genres
            tags {
                name
            }
            isAdult
            averageScore
            studios (isMain: true){
                nodes{
                    name
                }
            }
            nextAiringEpisode{
                episode
            }
            siteUrl
        }
    }
}"""


manga_query = """query ($id: Int,$search: String) {
    Page (perPage: 10) {
        media (id: $id, type: MANGA,search: $search) {
            id
            title {
                romaji
                english
                native
            }
            type
            format
            status
            description (asHtml: false)
            chapters
            volumes
            countryOfOrigin
            source
            genres
            isAdult
            averageScore
            siteUrl
        }
    }
}"""


character_query = """query ($id: Int, $search: String) {
  	Page {
	    characters (id: $id, search: $search) {
            id
            name {
                full
        	    native
      	    }
          	image {
                large
            }
      	    description
            gender
            dateOfBirth {
                year
                month
                day
            }
            age
            bloodType
      	    siteUrl
            favourites
            media {
                nodes {
                    title {
                        romaji
                        english
                        native
                    }
                    type
                    format
                    siteUrl
                }
            }
        }
    }
}"""


airing_query = """query ($id: Int, $idMal:Int, $search: String) {
    Media (id: $id, idMal: $idMal, search: $search, type: ANIME) {
        id
        title {
            romaji
            english
            native
        }
        status
        episodes
        countryOfOrigin
        nextAiringEpisode {
            airingAt
            timeUntilAiring
            episode
        }
    }
}"""


anilist_user_query = """query($id: Int, $search: String) {
	User(id: $id, name: $search) {
		id
		name
        siteUrl
        statistics {
            anime {
                count
                meanScore
                minutesWatched
                episodesWatched
            }
            manga {
                count
                meanScore
                chaptersRead
                volumesRead
            }
        }
	}
}"""


def is_valid_url(text: str) -> bool:
    try:
        result = urlparse(text)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def post_request(query: str, search_term: str):
    url = "https://graphql.anilist.co"
    variables = {"search": search_term}
    r = httpx.post(url, json={"query": query, "variables": variables})
    if r.status_code != 200:
        return None
    return r.json()


def get_country_flag(country: str) -> str:
    base = ord('🇦')
    emoji_flag = "".join(chr(base + ord(letter) - ord("A")) for letter in country)
    return emoji_flag


def get_date(data: dict) -> str:
    try:
        year = data["year"] or ""
        if not year and not data["month"]:
            return "N/A"
        day = data["day"]
        if 10 <= day % 100 <= 20:
            day = f"{day}th"
        else:
            day_dict = {1: "st", 2: "nd", 3: "rd"}
            day = f"{day}{day_dict.get(day % 10, 'th')}"
        month_name = calendar.month_name[int(data["month"])]
        return f"{day} {month_name} {year}"
    except:
        return "N/A"


def search_anime_filler(search_term: str):
    BASE = "https://www.animefillerlist.com/shows/"

    response = httpx.get(BASE).text
    soup = BeautifulSoup(response, "html.parser")
    div = soup.findAll("div", {"class": "Group"})

    index = {}
    for i in div:
        li = i.findAll("li")
        for j in li:
            index[j.text] = j.a["href"].split("/")[-1]

    results = {}
    keys = list(index.keys())
    for i in range(len(keys)):
        if search_term.lower() in keys[i].lower():
            results[keys[i]] = index[keys[i]]

    for result in results.keys():
        data = []
        response = httpx.get(BASE + results[result]).text
        soup = BeautifulSoup(response, "html.parser")
        base_div = soup.find("div", {"id": "Condensed"})

        if not base_div:
            continue

        divs = base_div.findAll("div")
        for div in divs:
            heading = div.find("span", {"class": "Label"}).text
            episodes = div.find("span", {"class": "Episodes"}).text
            data.append((heading, episodes))

        yield result, data


async def get_filler_info(search_term: str) -> str:
    animes = search_anime_filler(search_term)
    message = ""

    for anime in animes:
        html_message = f"<h1>{Symbols.check_mark} {anime[0]} Filler Guide:</h1>\n\n"

        for data in anime[1]:
            html_message += (
                f"<h3>{Symbols.bullet} {data[0]}:</h3> \n<code>{data[1]}</code>\n\n"
            )

        paste = post_to_telegraph(anime[0] + " Filler Guide", html_message)
        message += f"{Symbols.anchor} [{anime[0]}]({paste})\n"

    return message


def search_watch_order(anime: str):
    response = httpx.get(f"https://www.animechrono.com/search?q={quote(anime)}")
    soup = BeautifulSoup(response.text, "html.parser")

    item_div = soup.find("div", {"class": "search-result-items"})
    animes = item_div.find_all("a", {"class": "list-item search w-inline-block"})

    for anime in animes:
        name = anime.find("h1", "h1 search").text
        yield name, anime["href"]


async def get_watch_order(search_term: str) -> str:
    animes = search_watch_order(search_term)
    message = ""

    for anime in animes:
        message += f"**{Symbols.anchor} {anime[0]}:** \n"
        response = httpx.get("https://www.animechrono.com" + anime[1]).text
        soup = BeautifulSoup(response, "html.parser")

        elements = soup.find_all("h2", {"class": "heading-5"})
        for element in elements:
            message += f"    {Symbols.bullet} `{element.text}`\n"
        message += "\n"

    return message


async def get_anime_info(search_term: str) -> tuple[str, str]:
    data = post_request(anime_query, search_term)
    if not data:
        return "", ""

    data = data["data"]["Page"]["media"][0]
    english_title = data["title"]["english"]
    native_title = data["title"]["native"]
    if not english_title:
        english_title = data["title"]["romaji"]
    flag = get_country_flag(data["countryOfOrigin"])
    name = f"**[{flag}] {english_title} ({native_title})**"

    anime_id = data["id"]
    score = data["averageScore"] if data["averageScore"] else "N/A"
    source = str(data["source"]).title() if data["source"] else "N/A"
    mtype = str(data["type"]).title() if data["type"] else "N/A"
    synopsis = data["description"]

    episodes = data["episodes"]
    if not episodes:
        try:
            episodes = data["nextAiringEpisode"]["episode"] - 1
        except:
            episodes = "N/A"

    duration = data["duration"] if data["duration"] else "N/A"
    status = str(data["status"]).title() if data["status"] else "N/A"
    format = str(data["format"]).title() if data["format"] else "N/A"
    genre = ", ".join(data["genres"]) if data["genres"] else "N/A"
    tags = ", ".join([i["name"] for i in data["tags"][:5]]) if data["tags"] else "N/A"
    studio = data["studios"]["nodes"][0]["name"] if data["studios"]["nodes"] else "N/A"
    siteurl = f"[Anilist Website]({data['siteUrl']})" if data["siteUrl"] else "N/A"
    isAdult = data["isAdult"]

    trailer = "N/A"
    if data["trailer"] and data["trailer"]["site"] == "youtube":
        trailer = f"[Youtube](https://youtu.be/{data['trailer']['id']})"

    response = httpx.get(f"https://img.anili.st/media/{anime_id}").content
    banner = f"anime_{anime_id}.jpg"
    with open(banner, "wb") as f:
        f.write(response)

    description = post_to_telegraph(name, synopsis)

    message = await anime_template(
        name=name,
        score=score,
        source=source,
        mtype=mtype,
        episodes=episodes,
        duration=duration,
        status=status,
        format=format,
        genre=genre,
        studio=studio,
        trailer=trailer,
        siteurl=siteurl,
        description=description,
        tags=tags,
        isAdult=isAdult,
    )

    return message, banner


async def get_manga_info(search_term: str) -> tuple[str, str]:
    data = post_request(manga_query, search_term)
    if not data:
        return "", ""

    data = data["data"]["Page"]["media"][0]
    english_title = data["title"]["english"]
    native_title = data["title"]["native"]
    if not english_title:
        english_title = data["title"]["romaji"]
    flag = get_country_flag(data["countryOfOrigin"])
    name = f"**[{flag}] {english_title} ({native_title})**"

    manga_id = data["id"]
    score = data["averageScore"] if data["averageScore"] else "N/A"
    source = str(data["source"]).title() if data["source"] else "N/A"
    mtype = str(data["type"]).title() if data["type"] else "N/A"
    synopsis = data["description"]

    chapters = data["chapters"] if data["chapters"] else "N/A"
    volumes = data["volumes"] if data["volumes"] else "N/A"
    status = str(data["status"]).title() if data["status"] else "N/A"
    format = str(data["format"]).title() if data["format"] else "N/A"
    genre = ", ".join(data["genres"]) if data["genres"] else "N/A"
    siteurl = f"[Anilist Website]({data['siteUrl']})" if data["siteUrl"] else "N/A"
    isAdult = data["isAdult"]

    response = httpx.get(f"https://img.anili.st/media/{manga_id}").content
    banner = f"manga_{manga_id}.jpg"
    with open(banner, "wb") as f:
        f.write(response)

    description = post_to_telegraph(name, synopsis)

    message = await manga_templates(
        name=name,
        score=score,
        source=source,
        mtype=mtype,
        chapters=chapters,
        volumes=volumes,
        status=status,
        format=format,
        genre=genre,
        siteurl=siteurl,
        description=description,
        isAdult=isAdult,
    )

    return message, banner


async def get_character_info(search_term: str) -> tuple[str, str]:
    data = post_request(character_query, search_term)
    if not data:
        return "", ""

    data = data["data"]["Page"]["characters"][0]
    name = f"**{data['name']['full']} ({data['name']['native']})**"
    char_id = data["id"]

    description = data["description"].split("\n\n", 1)[0]
    gender = data["gender"] if data["gender"] else "N/A"
    date_of_birth = get_date(data["dateOfBirth"])
    age = data["age"] if data["age"] else "N/A"
    blood_type = data["bloodType"] if data["bloodType"] else "N/A"
    siteurl = f"[Anilist Website]({data['siteUrl']})" if data["siteUrl"] else "N/A"
    favorites = data["favourites"] if data["favourites"] else "N/A"

    cameo = data["media"]["nodes"][0] if data["media"]["nodes"] else {}
    if cameo:
        role_in = f"\n╰➢ **𝖱𝗈𝗅𝖾 𝖨𝗇:** [{cameo['title']['romaji']}]({cameo['siteUrl']})"
    else:
        role_in = ""

    response = httpx.get(data["image"]["large"]).content
    banner = f"character_{char_id}.jpg"
    with open(banner, "wb") as f:
        f.write(response)

    message = await character_templates(
        name=name,
        gender=gender,
        date_of_birth=date_of_birth,
        age=age,
        blood_type=blood_type,
        favorites=favorites,
        siteurl=siteurl,
        role_in=role_in,
        description=description,
    )

    return message, banner


async def get_airing_info(search_term: str) -> tuple[str, str]:
    data = post_request(airing_query, search_term)
    if not data:
        return "", ""

    data = data["data"]["Media"]
    english_title = data["title"]["english"]
    native_title = data["title"]["native"]
    if not english_title:
        english_title = data["title"]["romaji"]
    flag = get_country_flag(data["countryOfOrigin"])
    name = f"**[{flag}] {english_title} ({native_title})**"

    episode = data["episodes"]
    if not episode:
        try:
            episode = data["nextAiringEpisode"]["episode"]
        except:
            episode = "N/A"

    response = httpx.get(f"https://img.anili.st/media/{data['id']}").content
    banner = f"airing_{data['id']}.jpg"
    with open(banner, "wb") as f:
        f.write(response)

    status = str(data["status"]).title() if data["status"] else "N/A"
    next_date = data["nextAiringEpisode"]["airingAt"] if data["nextAiringEpisode"] else ""

    airing_info = ""
    if next_date:
        airing_info = f"\n**🗓️ {time.ctime(next_date)}**"

    message = await airing_templates(
        name=name,
        status=status,
        episode=episode,
        airing_info=airing_info,
    )

    return message, banner


async def get_anilist_user_info(search_term: str) -> tuple[str, str]:
    data = post_request(anilist_user_query, search_term)
    if not data:
        return "", ""

    data = data["data"]["User"]
    user_id = data["id"]
    name = data['name']
    siteurl = f"[Anilist Website]({data['siteUrl']})" if data["siteUrl"] else "N/A"

    response = httpx.get(f"https://img.anili.st/user/{user_id}").content
    banner = f"aniuser_{user_id}.jpg"
    with open(banner, "wb") as f:
        f.write(response)

    anime_stats = data["statistics"]["anime"]
    manga_stats = data["statistics"]["manga"]

    anime = (
        anime_stats["count"] or 0,
        anime_stats["meanScore"] or 0,
        anime_stats["minutesWatched"] or 0,
        anime_stats["episodesWatched"] or 0,
    )
    manga = (
        manga_stats["count"] or 0,
        manga_stats["meanScore"] or 0,
        manga_stats["chaptersRead"] or 0,
        manga_stats["volumesRead"] or 0,
    )

    message = await anilist_user_templates(name, anime, manga, siteurl)

    return message, banner
