import requests
from html_telegraph_poster import TelegraphPoster


def post_to_telegraph(
    title: str,
    content: str,
    author: str = "[ 𝖧𝖾𝗅𝗅𝖡𝗈𝗍 ]",
    url: str = "https://t.me/Its_HellBot",
) -> str:
    client = TelegraphPoster(use_api=True)
    client.create_api_token(author)
    response = client.post(title, author, content, url)
    return str(response["url"]).replace("telegra.ph", "te.legra.ph")


def spaceBin(data: str, extension: str = "none") -> str:
    data = {
        "content": data,
        "extension": extension,
    }

    resp = requests.post("https://spaceb.in/api/v1/documents/", data)

    try:
        result = resp.json()
        url = f"https://spaceb.in/{result['payload']['id']}"
    except Exception:
        url = ""

    return url
