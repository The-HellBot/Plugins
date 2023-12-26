import math
import re


def format_text(text: str) -> str:
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251"  # enclosed characters
        "]+",
        flags=re.UNICODE,
    )

    return re.sub(emoji_pattern, "", text)


def superscript(text: str) -> str:
    superscript_digits = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    return text.translate(superscript_digits)


def subscript(text: str) -> str:
    subscript_digits = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    return text.translate(subscript_digits)


def readable_time(seconds: int) -> str:
    count = 0
    out_time = ""
    time_list = []
    time_suffix_list = ["secs", "mins", "hrs", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]

    if len(time_list) == 4:
        out_time += time_list.pop() + ", "

    time_list.reverse()
    out_time += " ".join(time_list)

    return out_time or "0 secs"


def humanbytes(size: int):
    if not size:
        return ""
    power = 2**10
    number = 0
    dict_power_n = {0: " ", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        number += 1
    return str(round(size, 2)) + " " + dict_power_n[number] + "B"


def add_to_dict(data: dict, keys: list, value: str | int | bool = None) -> None:
    current_level = data
    for key in keys[:-1]:
        current_level = current_level.setdefault(key, {})
    current_level[keys[-1]] = value


def get_from_dict(data: dict, key: list):
    current_level = data
    for k in key:
        current_level = current_level[k]
    return current_level


def limit_per_page(limit: int) -> int:
    return math.ceil(limit / 10)


def secs_to_mins(secs: int) -> str:
    mins, secs = divmod(secs, 60)
    return f"{mins}:{secs}"
