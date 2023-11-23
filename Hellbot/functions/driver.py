import random
import time
from urllib.parse import quote_plus

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from Hellbot.core import Config

from .formatter import format_text


class ChromeDriver:
    def __init__(self) -> None:
        self.carbon_theme = [
            "3024-night", "a11y-dark", "blackboard",
            "base16-dark", "base16-light", "cobalt",
            "duotone-dark", "hopscotch", "lucario",
            "material", "monokai", "night-owl",
            "nord", "oceanic-next", "one-light",
            "one-dark", "panda-syntax", "paraiso-dark",
            "seti", "shades-of-purple", "solarized+dark",
            "solarized+light", "synthwave-84", "twilight",
            "verminal", "vscode", "yeti", "zenburn",
        ]

    def get(self):
        if not Config.CHROME_BIN:
            return (
                None,
                "ChromeBinaryErr: No binary path found! Install Chromium or Google Chrome.",
            )

        try:
            chrome_options = Options()
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--window-size=1920x1080")
            chrome_options.add_experimental_option(
                "prefs", {"download.default_directory": "./"}
            )
            chrome_options.binary_location = Config.CHROME_BIN
            driver = webdriver.Chrome(
                executable_path=Config.CHROME_DRIVER, options=chrome_options
            )
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
        driver.find_element(By.XPATH, "//input[@title='filename']").send_keys(filename)
        driver.find_element(By.XPATH, "//button[@id='export-png']").click()

        return f"{Config.DWL_DIR}/{filename}.png"


Driver = ChromeDriver()
