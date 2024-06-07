import asyncio
import json
import requests
from base64 import b64decode as m
from pyrogram import Client
from pyrogram.types import Message
from . import on_message, hellbot, HelpMenu

# Define the Gemini API function
def gemini(args: str) -> str:
    url = m(
        "aHR0cHM6Ly9nZW5lcmF0aXZlbGFuZ3VhZ2UuZ29vZ2xlYXBpcy5jb20vdjFiZXRhL21vZGVscy9nZW1pbmktcHJvOmdlbmVyYXRlQ29udGVudD9rZXk9QUl6YVN5QlFhb1VGLUtXalBWXzRBQnRTTjBEUTBSUGtOZUNoNHRN"
    ).decode("utf-8")
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": args}]}]}

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        generated_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        return generated_text
    else:
        return "Failed to generate text using Gemini API."

@on_message("gemi", allow_stan=True)
async def gemini_handler(client: Client, message: Message):
    user_input = message.text.split(None, 1)
    if len(user_input) < 2:
        hell = await hellbot.edit(
            message,
            "Please provide input text to generate a response."
        )
        await asyncio.sleep(10)
        await msg.delete()
        return
    user_input = user_input[1]

    hell = await hellbot.edit(message, "Generating response...")

    try:
        generated_text = gemini(user_input)
    except Exception as e:
        hell = await hellbot.edit(message, f"Error generating response: {e}")
        await asyncio.sleep(10)
        await msg.delete()
        return

    if "Failed to generate text" in generated_text:
        hell = await hellbot.edit(message, generated_text)
        await asyncio.sleep(10)
        await hell.delete()
        return

    output = f"➜ Input: {user_input}\n\n➜ Response:\n{generated_text}"
    msg = await hellbot.edit(message, f"{output}")
    await hell.delete()

HelpMenu("gemi").add(
    "gemi", "<text>", "Generates text using the Gemini language model!"
).done()
