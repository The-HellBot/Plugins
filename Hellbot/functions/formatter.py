def readable_time(seconds: int) -> str:
    count = 0
    out_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

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
    out_time += ":".join(time_list)

    return out_time


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
