import os
import time

from pyrogram.types import Message
from PIL import Image
from Hellbot.core import Config

from .tools import runcmd


async def convert_to_gif(file: str, is_video: bool = False) -> str:
    resultFileName = f"gif_{round(time.time())}.mp4"

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


async def image_to_sticker(file: str, max_size: tuple = (512, 512)) -> tuple[bool, str]:
    try:
        with Image.open(file) as img:
            original_width, original_height = img.size

            new_width = min(original_width, max_size[0])
            new_height = min(original_height, max_size[1])

            if original_width > max_size[0] or original_height > max_size[1]:
                img = img.resize((new_width, new_height), Image.LANCZOS)

            file_name = f"sticker_{int(time.time())}.png"
            img.save(file_name, "PNG")

        return True, file_name

    except Exception as e:
        return False, str(e)


async def video_to_png(
    file: str, duration: float, output: str = None
) -> tuple[str, bool]:
    resultFileName = output or f"{os.path.basename(file)}.png"
    cut_at = duration // 2

    cmd = f"ffmpeg -ss {cut_at} -i '{file}' -vframes 1 '{resultFileName}'"

    _, err, _, _ = await runcmd(cmd)
    if err:
        return err, False

    return resultFileName, True


async def video_to_sticker(file: Message) -> tuple[str, bool]:
    try:
        if file.animation:
            width, height = file.animation.width, file.animation.height
        elif file.video:
            width, height = file.video.width, file.video.height
        else:
            return "Unsupported media type.", False

        file_path = await file.download(Config.TEMP_DIR)
        output_path = os.path.join(Config.TEMP_DIR, "videoSticker.webm")

        if height > width:
            scale_params = f"scale=-1:512"
        else:
            scale_params = f"scale=512:-1"

        cmd = (
            f"ffmpeg -i {file_path} "
            f"-vf fps=30,{scale_params} -t 3 -c:v libvpx-vp9 -b:v 256k -an -pix_fmt yuv420p -auto-alt-ref 0 -loop 0 "
            f"-f webm {output_path}"
        )

        await runcmd(cmd)
        os.remove(file_path)

        return output_path, True

    except Exception as e:
        return f"Error during conversion: {e}", False
