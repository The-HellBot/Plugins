import asyncio
import math
import os
import shlex
import shutil
import time

from pyrogram.types import Message

from Hellbot.core import Config

from .formatter import humanbytes, readable_time


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


async def runcmd(cmd: str) -> tuple[str, str, int, int]:
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


async def update_dotenv(key: str, value: str) -> None:
    with open(".env", "r") as file:
        data = file.readlines()

    for index, line in enumerate(data):
        if line.startswith(f"{key}="):
            data[index] = f"{key}={value}\n"
            break

    with open(".env", "w") as file:
        file.writelines(data)


async def restart(update: bool = False):
    try:
        shutil.rmtree(Config.DWL_DIR)
        shutil.rmtree(Config.TEMP_DIR)
    except BaseException:
        pass

    cmd = (
        "git pull && pip3 install -U -r requirements.txt && bash start.sh"
        if update
        else "bash start.sh"
    )

    os.system(f"kill -9 {os.getpid()} && {cmd}")
