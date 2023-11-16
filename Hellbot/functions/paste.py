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
    return response["url"]
