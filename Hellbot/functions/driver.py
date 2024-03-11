import datetime
import json
import random
import re
import time
import urllib.parse
from urllib.parse import quote_plus
from typing import List
import os
import httpx
import requests
from pytz import country_names, country_timezones, timezone
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import \
    presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

from Hellbot.core import ENV, Config, db

from .formatter import format_text


class ChromeDriver:
    def __init__(self) -> None:
        self.carbon_theme = [
            "3024-night",
            "a11y-dark",
            "blackboard",
            "base16-dark",
            "base16-light",
            "cobalt",
            "duotone-dark",
            "hopscotch",
            "lucario",
            "material",
            "monokai",
            "night-owl",
            "nord",
            "oceanic-next",
            "one-light",
            "one-dark",
            "panda-syntax",
            "paraiso-dark",
            "seti",
            "shades-of-purple",
            "solarized+dark",
            "solarized+light",
            "synthwave-84",
            "twilight",
            "verminal",
            "vscode",
            "yeti",
            "zenburn",
        ]

    def get(self):
        if not Config.CHROME_BIN:
            return (
                None,
                "ChromeBinaryErr: No binary path found! Install Chromium or Google Chrome.",
            )

        try:
            options = Options()
            options.binary_location = Config.CHROME_BIN
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--disable-gpu")
            options.add_argument("--headless=new")
            options.add_argument("--test-type")
            options.add_argument("--no-sandbox")
            options.add_argument("--window-size=1920x1080")
            options.add_experimental_option(
                "prefs", {"download.default_directory": "./"}
            )
            service = Service(Config.CHROME_DRIVER)
            driver = webdriver.Chrome(options, service)
            return driver, None
        except Exception as e:
            return None, f"ChromeDriverErr: {e}"

    def close(self, driver: webdriver.Chrome):
        driver.close()
        driver.quit()

    @property
    def get_random_carbon(self) -> str:
        url = "https://carbon.now.sh/?l=auto"
        url += f"&t={random.choice(self.carbon_theme)}"
        url += f"&bg=rgba%28{random.randint(1, 255)}%2C{random.randint(1, 255)}%2C{random.randint(1, 255)}%2C1%29"
        url += "&code="
        return url

    async def generate_carbon(
        self, driver: webdriver.Chrome, code: str, is_random: bool = False
    ) -> str:
        filename = f"{round(time.time())}"
        BASE_URL = (
            self.get_random_carbon
            if is_random
            else "https://carbon.now.sh/?l=auto&code="
        )

        driver.get(BASE_URL + format_text(quote_plus(code)))
        driver.command_executor._commands["send_command"] = (
            "POST",
            "/session/$sessionId/chromium/send_command",
        )
        params = {
            "cmd": "Page.setDownloadBehavior",
            "params": {"behavior": "allow", "downloadPath": Config.DWL_DIR},
        }
        driver.execute("send_command", params)

        driver.find_element(By.XPATH, "//button[@id='export-menu']").click()
        driver.find_element(
            By.XPATH, "//input[@title='filename']").send_keys(filename)
        driver.find_element(By.XPATH, "//button[@id='export-png']").click()

        return f"{Config.DWL_DIR}/{filename}.png"


class ClimateDriver:
    def __init__(self) -> None:
        self.weather_api = "https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid={2}&units=metric"
        self.location_api = (
            "https://api.openweathermap.org/geo/1.0/direct?q={0}&limit=1&appid={1}"
        )
        self.pollution_api = "http://api.openweathermap.org/data/2.5/air_pollution?lat={0}&lon={1}&appid={2}"
        self.AQI_DICT = {
            1: "Good",
            2: "Fair",
            3: "Moderate",
            4: "Poor",
            5: "Very Poor",
        }

    async def fetchLocation(self, city: str, apiKey: str):
        response = httpx.get(self.location_api.format(city, apiKey))
        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0]["lat"], data[0]["lon"]
        return None, None

    async def fetchWeather(self, city: str, apiKey: str):
        lattitude, longitude = await self.fetchLocation(city, apiKey)
        if not lattitude and not longitude:
            return None

        response = httpx.get(self.weather_api.format(
            lattitude, longitude, apiKey))
        if response.status_code == 200:
            return response.json()
        return None

    async def fetchAirPollution(self, city: str, apiKey: str):
        lattitude, longitude = await self.fetchLocation(city, apiKey)
        if not lattitude and not longitude:
            return None

        response = httpx.get(self.pollution_api.format(
            lattitude, longitude, apiKey))
        if response.status_code == 200:
            return response.json()
        return None

    async def getTime(self, timestamp: int) -> str:
        tz = await db.get_env(ENV.time_zone) or "Asia/Kolkata"
        tz = timezone(tz)
        return datetime.datetime.fromtimestamp(timestamp, tz=tz).strftime("%I:%M %p")

    def getCountry(self, country_code: str) -> str:
        return country_names.get(country_code, "Unknown")

    def getCountryTimezone(self, country_code: str) -> str:
        timezones = country_timezones.get(country_code, [])
        if timezones:
            return ", ".join(timezones)
        return "Unknown"

    def getWindData(self, windSpeed: str, windDegree: str) -> str:
        dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        ix = round(windDegree / (360.00 / len(dirs)))
        kmph = str(float(windSpeed) * 3.6) + " km/h"
        return f"[{dirs[ix % len(dirs)]}] {kmph}"


class YoutubeDriver:
    def __init__(self, search_terms: str, max_results: int = 5):
        self.base_url = "https://youtube.com/results?search_query={0}"
        self.search_terms = search_terms
        self.max_results = max_results
        self.videos = self._search()

    def _search(self):
        encoded_search = urllib.parse.quote_plus(self.search_terms)
        response = requests.get(self.base_url.format(encoded_search)).text

        while "ytInitialData" not in response:
            response = requests.get(self.base_url.format(encoded_search)).text

        results = self._parse_html(response)

        if self.max_results is not None and len(results) > self.max_results:
            return results[: self.max_results]

        return results

    def _parse_html(self, response: str):
        results = []
        start = response.index("ytInitialData") + len("ytInitialData") + 3
        end = response.index("};", start) + 1
        json_str = response[start:end]
        data = json.loads(json_str)

        videos = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"][
            "sectionListRenderer"
        ]["contents"][0]["itemSectionRenderer"]["contents"]

        for video in videos:
            res = {}
            if "videoRenderer" in video.keys():
                video_data = video.get("videoRenderer", {})
                _id = video_data.get("videoId", None)

                res["id"] = _id
                res["thumbnail"] = f"https://i.ytimg.com/vi/{_id}/hqdefault.jpg"
                res["title"] = (
                    video_data.get("title", {}).get(
                        "runs", [[{}]])[0].get("text", None)
                )
                res["channel"] = (
                    video_data.get("longBylineText", {})
                    .get("runs", [[{}]])[0]
                    .get("text", None)
                )
                res["duration"] = video_data.get(
                    "lengthText", {}).get("simpleText", 0)
                res["views"] = video_data.get("viewCountText", {}).get(
                    "simpleText", "Unknown"
                )
                res["publish_time"] = video_data.get("publishedTimeText", {}).get(
                    "simpleText", "Unknown"
                )
                res["url_suffix"] = (
                    video_data.get("navigationEndpoint", {})
                    .get("commandMetadata", {})
                    .get("webCommandMetadata", {})
                    .get("url", None)
                )

                results.append(res)
        return results

    def to_dict(self, clear_cache=True) -> list[dict]:
        result = self.videos
        if clear_cache:
            self.videos = []
        return result

    @staticmethod
    def check_url(url: str) -> tuple[bool, str]:
        if "&" in url:
            url = url[: url.index("&")]

        if "?si=" in url:
            url = url[: url.index("?si=")]

        youtube_regex = (
            r"(https?://)?(www\.)?"
            r"(youtube|youtu|youtube-nocookie)\.(com|be)/"
            r'(video|embed|shorts/|watch\?v=|v/|e/|u/\\w+/|\\w+/)?([^"&?\\s]{11})'
        )
        match = re.match(youtube_regex, url)
        if match:
            return True, match.group(6)
        else:
            return False, "Invalid YouTube URL!"

    @staticmethod
    def song_options() -> dict:
        return {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "480",
                }
            ],
            "outtmpl": "%(id)s",
            "quiet": True,
            "logtostderr": False,
        }

    @staticmethod
    def video_options() -> dict:
        return {
            "format": "best",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": "mp4",
                }
            ],
            "outtmpl": "%(id)s.mp4",
            "quiet": True,
            "logtostderr": False,
        }


class SCRAP_DATA:
    """Class to get and handel scrapped data"""

    def __init__(self, urls: List[str] or str) -> None:
        self.urls = urls
        self.path = "./scrapped/"
        if not os.path.isdir(self.path):
            os.makedirs("./scrapped/")

    def get_images(self) -> list:
        images = []
        if isinstance(self.urls, str):
            requested = requests.get(self.urls)
            try:
                name = self.path + f"img_{time.time()}.jpg"
                with open(name, "wb") as f:
                    f.write(requested.content)
                images.append(name)
            except Exception as e:
                requested.close()
        else:
            for i in self.urls:
                if i:
                    requested = requests.get(i)
                else:
                    continue
                try:
                    name = self.path + f"img_{time.time()}.jpg"
                    with open(name, "wb") as f:
                        f.write(requested.content)
                    images.append(name)
                except Exception as e:

                    requested.close()
                    continue
        return images

    def get_videos(self) -> list:
        videos = []
        if isinstance(self.urls, str):
            if i:
                requested = requests.get(i)
            else:
                return []
            try:
                name = self.path + f"vid_{time.time()}.mp4"
                with open(name, "wb") as f:
                    f.write(requested.content)
                videos.append(name)
            except Exception as e:
                requested.close()
        else:
            for i in self.urls:
                if i:
                    requested = requests.get(i)
                else:
                    continue
                try:
                    name = self.path + f"vid_{time.time()}.mp4"
                    with open(name, "wb") as f:
                        f.write(requested.content)
                    videos.append(name)
                except Exception as e:

                    requested.close()
                    continue
        return videos


class INSTAGRAM(ChromeDriver):
    """Class to scrap data from instagram"""

    def __init__(self, url: str) -> None:
        self.url = url
        self.article = "article._aa6a"
        self.ul_class = "_acay"
        self.image_class = "x5yr21d"
        self.video_class = "x1lliihq"
        self.next_button = "button._afxw"
        self.return_dict = {"image": [], "video": []}
        super().__init__()

    def get_all(self):
        driver, error = self.get()
        if not driver:
            return error

        driver.get(self.url)
        wait = WebDriverWait(driver, 30)
        image_links = []
        video_links = []
        try:
            element = wait.until(presence_of_element_located(
                (By.CLASS_NAME, self.ul_class)))

            while True:
                sub_element = element.find_elements(
                    By.CLASS_NAME, self.image_class)
                for i in sub_element:
                    url = i.get_attribute("src")
                    image_links.append(url)

                sub_element = element.find_elements(
                    By.CLASS_NAME, self.video_class)
                for i in sub_element:
                    url = i.get_attribute("src")
                    video_links.append(url)

                try:
                    driver.find_element(
                        By.CSS_SELECTOR, self.next_button).click()
                except:  # Failed to either find the element or click on next i.e. no more media left in post
                    break
        except:
            element = wait.until(presence_of_element_located(
                By.CSS_SELECTOR, self.article))
            try:
                sub_element = element.find_element(By.TAG_NAME, "img")
                url = sub_element.get_attribute("src")
                image_links.append(url)
            except:
                sub_element = element.find_element(By.TAG_NAME, "video")
                url = sub_element.get_attribute("src")
                video_links.append(url)

        self.close(driver)
        # To remove duplicates here I am converting into set
        if image_links:
            image_links = list(set(image_links))
        if video_links:
            video_links = list(set(video_links))
            for i in video_links:
                image_links.remove(i)

        self.return_dict.get("image").extend(image_links)
        self.return_dict.get("video").extend(video_links)
        return self.return_dict


Driver = ChromeDriver()
Climate = ClimateDriver()
