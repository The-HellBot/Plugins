import math
import os
import time

from pyrogram.types import Message

from .formatter import readable_time, humanbytes


async def progress(
    current: int, total: int, message: Message, start: float, process: str
):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        complete_time = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + complete_time
        progress_str = "**[{0}{1}] : {2}%\n**".format(
            "".join(["●" for i in range(math.floor(percentage / 10))]),
            "".join(["○" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2),
        )
        msg = (
            progress_str
            + "__{0}__ **𝗈𝖿** __{1}__\n**𝖲𝗉𝖾𝖾𝖽:** __{2}/s__\n**𝖤𝖳𝖠:** __{3}__".format(
                humanbytes(current),
                humanbytes(total),
                humanbytes(speed),
                readable_time(estimated_total_time / 1000),
            )
        )
        await message.edit_text(f"**{process} ...**\n\n{msg}")


async def get_files_from_directory(directory: str) -> list:
    all_files = []
    for path, _, files in os.walk(directory):
        for file in files:
            all_files.append(os.path.join(path, file))
    return all_files
