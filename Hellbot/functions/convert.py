import time

from .tools import runcmd


async def convert_to_gif(file: str, is_video: bool = False) -> str:
    resultFileName = f"gif_{round(time.time())}.gif"

    if is_video:
        cmd = f"ffmpeg -i '{file}' -c copy '{resultFileName}'"
    else:
        cmd = f"lottie_convert.py '{file}' '{resultFileName}'"

    await runcmd(cmd)

    return resultFileName

