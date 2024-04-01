import uuid

import requests

from .utility import TGraph


def post_to_telegraph(
    title: str,
    content: str,
    author: str = "[ 𝖧𝖾𝗅𝗅𝖡𝗈𝗍 ]",
    url: str = "https://t.me/Its_HellBot",
) -> str:
    content = content.replace("\n", "<br>")
    try:
        response = TGraph.telegraph.create_page(
            title=title,
            html_content=content,
            author_name=author,
            author_url=url,
        )
    except Exception:
        rnd_key = uuid.uuid4().hex[:8]
        title = f"{title}_{rnd_key}"
        response = TGraph.telegraph.create_page(
            title=title,
            html_content=content,
            author_name=author,
            author_url=url,
        )

    return f"https://te.legra.ph/{response['path']}"


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
