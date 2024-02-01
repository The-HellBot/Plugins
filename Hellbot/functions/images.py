import calendar
import os
import random
import textwrap
import time
from unidecode import unidecode
import httpx
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

from .formatter import format_text, limit_per_page


def convert_to_png(image: str) -> str:
    output_img = f"png_{round(time.time())}.png"

    img = Image.open(image)
    img.save(output_img, "PNG")
    img.close()

    os.remove(image)
    return output_img


def add_rounded_corners(img: Image.Image, radius: int = 80):
    circle = Image.new("L", (radius * 2, radius * 2), 0)

    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)

    alpha = Image.new("L", img.size, 255)
    w, h = img.size

    alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
    alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
    alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
    alpha.paste(
        circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius)
    )

    img.putalpha(alpha)

    return img


def generate_alive_image(
    username: str, profile_pic: str, del_img: bool, font_path: str
) -> str:
    if not profile_pic.endswith(".png"):
        profile_pic = convert_to_png(profile_pic)

    img = Image.open(profile_pic).convert("RGBA")
    img_rotated = img.rotate(45, expand=True)

    width, height = img_rotated.size
    left = width / 2 - 480 / 2
    top = height / 2 - 480 / 2
    right = width / 2 + 480 / 2
    bottom = height / 2 + 480 / 2

    cropped_img = img_rotated.crop((left, top, right, bottom))

    img_rotated = ImageOps.fit(
        cropped_img, (480, 480), method=0, bleed=0.0, centering=(0.5, 0.5)
    )

    img_rounded = add_rounded_corners(img_rotated)

    img = img_rounded.rotate(-45, expand=True)

    background = Image.open("./Hellbot/resources/images/hellbot_alive.png").convert(
        "RGBA"
    )

    background.paste(img, (383, 445), img)
    draw = ImageDraw.Draw(background)

    text = format_text(username[:25] + ("..." if len(username) > 25 else ""))

    font_size = width // 15
    font = ImageFont.truetype(font_path, font_size, encoding="utf-8")

    text_length = draw.textlength(text, font)
    position = ((background.width - text_length) / 2, background.height - 145)
    draw.text(
        position,
        unidecode(text),
        (255, 255, 255),
        font,
    )

    output_img = f"alive_{int(time.time())}.png"
    background.save(output_img, "PNG")
    background.close()

    if del_img:
        os.remove(profile_pic)

    return output_img


async def get_wallpapers(
    access: str,
    limit: int,
    query: str = "",
    isRandom: bool = False,
) -> list[str]:
    headers = {"Authorization": f"Client-ID {access}"}

    if isRandom:
        api = f"https://api.unsplash.com/photos/random?count={limit}"
        response = httpx.get(api, headers=headers)
        results = response.json()
        urls = [i["urls"]["raw"] for i in results]
    else:
        api = f"https://api.unsplash.com/search/photos?query={query}&page={limit_per_page(limit)}"
        response = httpx.get(api, headers=headers)
        result = response.json()
        urls = [i["urls"]["raw"] for i in result["results"]]

    random.shuffle(urls)

    return urls[:limit]


async def deep_fry(img: Image.Image) -> Image.Image:
    colours = (
        (random.randint(50, 200), random.randint(40, 170), random.randint(40, 190)),
        (random.randint(190, 255), random.randint(170, 240), random.randint(180, 250)),
    )

    img = img.copy().convert("RGB")
    img = img.convert("RGB")

    width, height = img.width, img.height

    img = img.resize(
        (
            int(width ** random.uniform(0.8, 0.9)),
            int(height ** random.uniform(0.8, 0.9)),
        ),
        resample=Image.LANCZOS,
    )

    img = img.resize(
        (
            int(width ** random.uniform(0.85, 0.95)),
            int(height ** random.uniform(0.85, 0.95)),
        ),
        resample=Image.BILINEAR,
    )

    img = img.resize(
        (
            int(width ** random.uniform(0.89, 0.98)),
            int(height ** random.uniform(0.89, 0.98)),
        ),
        resample=Image.BICUBIC,
    )

    img = img.resize((width, height), resample=Image.BICUBIC)
    img = ImageOps.posterize(img, random.randint(3, 7))

    overlay = img.split()[0]
    overlay = ImageEnhance.Contrast(overlay).enhance(random.uniform(1.0, 2.0))
    overlay = ImageEnhance.Brightness(overlay).enhance(random.uniform(1.0, 2.0))
    overlay = ImageOps.colorize(overlay, colours[0], colours[1])

    img = Image.blend(img, overlay, random.uniform(0.1, 0.4))
    img = ImageEnhance.Sharpness(img).enhance(random.randint(5, 300))

    return img


async def make_logo(background: str, text: str, font_path: str) -> str:
    if not background.endswith(".png"):
        background = convert_to_png(background)

    bg = Image.open(background).convert("RGBA")
    bgWidth, bgHeight = bg.size

    text = format_text(text)
    font_size = bgWidth // len(text)
    font = ImageFont.truetype(font_path, font_size, encoding="utf-8")

    draw = ImageDraw.Draw(bg)
    text_length = draw.textlength(text, font)

    x = (bgWidth - text_length) // 2
    y = (bgHeight - font_size) // 2

    draw.text(
        (x, y),
        unidecode(text),
        (255, 255, 255),
        font,
        stroke_fill=(0, 0, 0),
        stroke_width=2,
    )

    output_img = f"logo_{int(time.time())}.png"
    bg.save(output_img, "PNG")
    bg.close()

    os.remove(background)

    return output_img


async def draw_meme(
    image_path: str, upper_text: str = "", lower_text: str = ""
) -> list[str]:
    image = Image.open(image_path)
    width, height = image.size

    draw = ImageDraw.Draw(image)
    font_size = int((30 / 500) * width)
    font = ImageFont.truetype("./Hellbot/resources/fonts/Montserrat.ttf", font_size)

    curr_height, padding = 20, 5
    for utext in textwrap.wrap(upper_text, 25):
        upper_width = draw.textlength(utext, font=font)
        draw.text(
            ((width - upper_width) / 2, curr_height),
            unidecode(utext),
            (255, 255, 255),
            font,
            stroke_width=3,
            stroke_fill=(0, 0, 0),
        )
        curr_height += font_size + padding

    curr_height = height - font_size
    for ltext in reversed(textwrap.wrap(lower_text, 25)):
        lower_width = draw.textlength(ltext, font=font)
        draw.text(
            ((width - lower_width) / 2, curr_height - font_size),
            ltext,
            (255, 255, 255),
            font,
            stroke_width=3,
            stroke_fill=(0, 0, 0),
        )
        curr_height -= font_size + padding

    filename = f"meme_{int(time.time())}"
    image.save(f"{filename}.png", "PNG", optimize=True)
    image.save(f"{filename}.webp", "WEBP", optimize=True)
    image.close()

    return [f"{filename}.png", f"{filename}.webp"]


async def remove_bg(api_key: str, image: str) -> str:
    response = httpx.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": open(image, "rb")},
        data={"size": "auto"},
        headers={"X-Api-Key": api_key},
    )
    filename = f"removedbg_{int(time.time())}.png"

    if response.is_success:
        with open(filename, "wb") as f:
            f.write(response.content)
    else:
        raise Exception(
            f"RemoveBGError: [{response.status_code}] {response.content.decode('utf-8')}"
        )

    return filename


def create_gradient(
    size: tuple[int, int],
    color_start: tuple[int, int, int],
    color_end: tuple[int, int, int],
) -> Image.Image:
    gradient = Image.new("RGB", (size))
    draw = ImageDraw.Draw(gradient)

    for x in range(size[0]):
        r = int(color_start[0] + (color_end[0] - color_start[0]) * (x / size[0]))
        g = int(color_start[1] + (color_end[1] - color_start[1]) * (x / size[0]))
        b = int(color_start[2] + (color_end[2] - color_start[2]) * (x / size[0]))

        draw.line([(x, 0), (x, size[1])], fill=(r, g, b))

    return gradient


async def create_calendar(year: int, month: int) -> str:
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]

    calendar_image = create_gradient((500, 500), (140, 200, 250), (0, 150, 200))
    draw = ImageDraw.Draw(calendar_image)

    month_font = ImageFont.truetype("./Hellbot/resources/fonts/Montserrat.ttf", 40)
    month_x = (
        calendar_image.width - draw.textlength(f"{month_name} {year}", month_font)
    ) // 2
    month_y = 30
    draw.text(
        (month_x, month_y),
        f"{month_name} {year}",
        (43, 255, 136),
        month_font,
        stroke_width=2,
        stroke_fill=(255, 40, 40),
    )

    week_font = ImageFont.truetype("./Hellbot/resources/fonts/Montserrat.ttf", 23)
    weekdays_text = "   ".join([day[:3] for day in calendar.day_name])
    textsize = draw.textlength(weekdays_text, week_font)
    draw.text(
        ((calendar_image.width - textsize) // 2, month_y + 80),
        weekdays_text,
        (150, 190, 200),
        week_font,
        stroke_width=2,
        stroke_fill=(200, 150, 250),
    )

    scale_factor = 1.5
    cell_size = 30
    padding = 15

    font = ImageFont.truetype("./Hellbot/resources/fonts/Montserrat.ttf", 30)

    for week_num, week in enumerate(cal):
        for day_num, day in enumerate(week):
            x = int(day_num * (cell_size + padding) * scale_factor)
            y = int((week_num + 3) * (cell_size + padding) * scale_factor)

            cell_width = int(cell_size * scale_factor)
            cell_height = int(cell_size * scale_factor)

            text_x = (
                int(x + (cell_width - draw.textlength(str(day), font=font)) // 2)
                + cell_size
            )
            text_y = (
                int(y + (cell_height - draw.textlength(str(day), font=font)) // 2) - 55
            )

            if day != 0:
                draw.text(
                    (text_x, text_y),
                    str(day),
                    (240, 200, 100),
                    font,
                    stroke_width=1,
                    stroke_fill=(0, 0, 0),
                )

    filename = f"calendar_{int(time.time())}.png"
    calendar_image.save(filename, "PNG")
    calendar_image.close()

    return filename


async def create_thumbnail(photo: str, xy: tuple[int, int], file_size: int):
    img = Image.open(photo)
    img.thumbnail(xy)

    size_in_bytes = file_size * 1024
    quality = 90

    while True:
        img.save(photo, "JPEG", quality=quality, optimize=True)
        if os.path.getsize(photo) <= size_in_bytes:
            break

        quality -= 5

    return photo