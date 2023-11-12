import os
import time

from PIL import Image, ImageDraw, ImageFont, ImageOps

from .formatter import formatted_text


def convert_to_png(image: str) -> str:
    img = Image.open(image)
    output_img = f"png_{round(time.time())}.png"
    img.save(output_img, "PNG")
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
    alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))

    img.putalpha(alpha)

    return img


def generate_alive_image(username: str, profile_pic: str, del_img: bool) -> str:
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

    img_rotated = ImageOps.fit(cropped_img, (480, 480), method=0, bleed=0.0, centering=(0.5, 0.5))

    img_rounded = add_rounded_corners(img_rotated)

    img = img_rounded.rotate(-45, expand=True)

    background = Image.open("./Hellbot/resources/images/hellbot_alive.png").convert("RGBA")

    background.paste(img, (383, 445), img)

    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype(
        "./Hellbot/resources/fonts/Montserrat.ttf", 60, encoding="utf-8"
    )

    text = formatted_text(username[:20] + ("..." if len(username) > 20 else ""))
    text_length = draw.textlength(text, font)

    position = ((background.width - text_length) / 2, background.height - 155)
    draw.text(position, text, (255, 255, 255), font=font)

    output_img = f"alive_{round(time.time())}.png"
    background.save(output_img, "PNG")

    if del_img: os.remove(profile_pic)

    return output_img
