import base64

from pyrogram.types import Message

from . import HelpMenu, hellbot, on_message


@on_message("base64enc", allow_stan=True)
async def base64enc(_, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await hellbot.delete(message, "Give me something to encode.")

    if len(message.command) >= 2:
        text = await hellbot.input(message)
    else:
        text = message.reply_to_message.text or message.reply_to_message.caption

    if not text:
        return await hellbot.delete(message, "Give me something to encode.")

    hell = await hellbot.edit(message, "Encoding...")

    encoded = base64.b64encode(text.encode()).decode()
    await hellbot.edit(hell, f"**𝖡𝖺𝗌𝖾64 𝖤𝗇𝖼𝗈𝖽𝖾𝖽:**\n\n`{encoded}`")


@on_message("base64dec", allow_stan=True)
async def base64dec(_, message: Message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await hellbot.delete(message, "Give me something to decode.")

    if len(message.command) >= 2:
        text = await hellbot.input(message)
    else:
        text = message.reply_to_message.text or message.reply_to_message.caption

    if not text:
        return await hellbot.delete(message, "Give me something to decode.")

    hell = await hellbot.edit(message, "Decoding...")

    decoded = base64.b64decode(text.encode()).decode()
    await hellbot.edit(hell, f"**𝖡𝖺𝗌𝖾64 𝖣𝖾𝖼𝗈𝖽𝖾𝖽:**\n\n`{decoded}`")


HelpMenu("tools").add(
    "base64enc",
    "<reply> or <text>",
    "Encode the text to a base64 string.",
    "base64enc Hello, World!",
).add(
    "base64dec",
    "<reply> or <text>",
    "Decode the base64 string to text.",
    "base64dec SGVsbG8sIFdvcmxkIQ==",
).info(
    "Basic Tools"
).done()
