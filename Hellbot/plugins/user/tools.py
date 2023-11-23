import base64, math

from pyrogram.types import Message

from Hellbot.core import Symbols

from . import HelpMenu, hellbot, on_message


math_cmds = ["sin", "cos", "tan", "square", "cube", "sqroot", "factorial", "power"]


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


@on_message(["calculate", "calc"], allow_stan=True)
async def calculator(_, message: Message):
    if len(message.command) < 2:
        return await hellbot.delete(message, "Give me something to calculate.")

    query = await hellbot.input(message)
    hell = await hellbot.edit(message, "Calculating...")
    try:
        result = eval(query)
    except Exception:
        result = "Invalid Expression"

    await hellbot.edit(
        hell, f"**{Symbols.bullet} 𝖤𝗑𝗉𝗋𝖾𝗌𝗌𝗂𝗈𝗇:** `{query}`\n\n**{Symbols.bullet} 𝖱𝖾𝗌𝗎𝗅𝗍:**\n`{result}`"
    )


@on_message("math", allow_stan=True)
async def maths(_, message: Message):
    if len(message.command) < 3:
        return await hellbot.delete(message, "Give me something to calculate.")

    cmd = message.command[1].lower()
    query = message.command[2].lower()

    if cmd not in math_cmds:
        return await hellbot.delete(message, f"**Unknown command!** \n\nAvailable Commands are: \n`{'`, `'.join(math_cmds)}`", 20)

    hell = await hellbot.edit(message, "Calculating...")

    if cmd == "sin":
        result = math.sin(int(query))
    elif cmd == "cos":
        result = math.cos(int(query))
    elif cmd == "tan":
        result = math.tan(int(query))
    elif cmd == "square":
        result = int(query) * int(query)
    elif cmd == "cube":
        result = int(query) * int(query) * int(query)
    elif cmd == "sqroot":
        result = math.sqrt(int(query))
    elif cmd == "factorial":
        result = math.factorial(int(query))
    elif cmd == "power":
        result = math.pow(int(query), 2)

    await hellbot.edit(
        hell, f"**{Symbols.bullet} 𝖤𝗑𝗉𝗋𝖾𝗌𝗌𝗂𝗈𝗇:** `{cmd} {query}`\n\n**{Symbols.bullet} 𝖱𝖾𝗌𝗎𝗅𝗍:**\n`{result}`"
    )


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
).add(
    "calculate",
    "<expression>",
    "Calculate the expression.",
    "calculate 69*100",
    "You can also use 'calc' as an alias.",
).add(
    "math",
    "<expression>",
    "Perform some basic math operations.",
    "math sin 90",
    f"Available Commands are: \n`{'`, `'.join(math_cmds)}`",
).info(
    "Basic Tools"
).done()
