import os
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


async def tgs_to_png(file: str) -> str:
    resultFileName = f"png_{round(time.time())}.png"

    cmd = f"lottie_convert.py '{file}' '{resultFileName}'"

    await runcmd(cmd)

    return resultFileName


async def video_to_png(file: str, duration: float, output: str = None) -> tuple[str, bool]:
    resultFileName = output or f"{os.path.basename(file)}.png"
    cut_at = duration // 2

    cmd = f"ffmpeg -ss {cut_at} -i '{file}' -vframes 1 '{resultFileName}'"

    _, err, _, _ = await runcmd(cmd)
    if err:
        return err, False

    return resultFileName, True
