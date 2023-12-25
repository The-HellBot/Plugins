from pyrogram.types import Message

from Hellbot.core import ENV
from Hellbot.functions.driver import Climate
from Hellbot.functions.formatter import subscript, superscript
from Hellbot.functions.templates import airpollution_templates, climate_templates

from . import HelpMenu, db, hellbot, on_message


@on_message("climate", allow_stan=True)
async def climate(_, message: Message):
    if len(message.command) < 2:
        city = "Delhi"
    else:
        city = await hellbot.input(message)

    hell = await hellbot.edit(message, f"**Fetching climate data for `{city}`**")

    apiKey = await db.get_env(ENV.climate_api)
    if not apiKey:
        return await hellbot.delete(
            hell, f"**Climate API not found!** Setup `{ENV.climate_api}` first."
        )

    data = await Climate.fetchWeather(city, apiKey)
    if not data:
        return await hellbot.delete(hell, f"**Climate data not found for `{city}`**")

    city_name = data["name"]
    country = Climate.getCountry(data["sys"]["country"])
    weather = data["weather"][0]["main"]
    timezone = Climate.getCountryTimezone(data["sys"]["country"])
    sunrise = await Climate.getTime(data["sys"]["sunrise"])
    sunset = await Climate.getTime(data["sys"]["sunset"])
    wind = Climate.getWindData(data["wind"]["speed"], data["wind"]["deg"])
    temperature = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    temp_min = data["main"]["temp_min"]
    temp_max = data["main"]["temp_max"]
    pressure = data["main"]["pressure"]
    humidity = data["main"]["humidity"]
    visibility = data["visibility"]
    clouds = data["clouds"]["all"]

    await hell.edit(
        await climate_templates(
            city_name=city_name,
            country=country,
            weather=weather,
            timezone=timezone,
            sunrise=sunrise,
            sunset=sunset,
            wind=wind,
            temperature=temperature,
            feels_like=feels_like,
            temp_min=temp_min,
            temp_max=temp_max,
            pressure=pressure,
            humidity=humidity,
            visibility=visibility,
            clouds=clouds,
        ),
        disable_web_page_preview=True,
    )


@on_message("airpollution", allow_stan=True)
async def airpollution(_, message: Message):
    if len(message.command) < 2:
        city = "Delhi"
    else:
        city = await hellbot.input(message)

    hell = await hellbot.edit(message, f"**Fetching air pollution data for `{city}`**")

    apiKey = await db.get_env(ENV.climate_api)
    if not apiKey:
        return await hellbot.delete(
            hell, f"**Climate API not found!** Setup `{ENV.climate_api}` first."
        )

    data = await Climate.fetchAirPollution(city, apiKey)
    if not data:
        return await hellbot.delete(
            hell, f"**Air pollution data not found for `{city}`**"
        )

    data = data["list"][0]
    ugm3 = superscript("µg/m³")
    sub2_5 = subscript("2.5")
    sub10 = subscript("10")

    city_name = city.upper()
    aqi_index = data["main"]["aqi"]
    aqi_cond = Climate.AQI_DICT[aqi_index]
    aqi = f"{aqi_index} ({aqi_cond})"
    co = f"{data['components']['co']} {ugm3}"
    no = f"{data['components']['no']} {ugm3}"
    no2 = f"{data['components']['no2']} {ugm3}"
    o3 = f"{data['components']['o3']} {ugm3}"
    so2 = f"{data['components']['so2']} {ugm3}"
    nh3 = f"{data['components']['nh3']} {ugm3}"
    pm2_5 = data["components"]["pm2_5"]
    pm10 = data["components"]["pm10"]

    await hell.edit(
        await airpollution_templates(
            city_name=city_name,
            aqi=aqi,
            co=co,
            no=no,
            no2=no2,
            o3=o3,
            so2=so2,
            nh3=nh3,
            pm2_5=pm2_5,
            pm10=pm10,
            sub2_5=sub2_5,
            sub10=sub10,
        ),
        disable_web_page_preview=True,
    )


HelpMenu("climate").add(
    "climate",
    "<city name>",
    "Get climate data of a city.",
    "climate Delhi",
    "City name is optional. Bydefault Delhi's climate data will be fetched.",
).add(
    "airpollution",
    "<city name>",
    "Get air pollution data of a city.",
    "airpollution Delhi",
    "City name is optional. Bydefault Delhi's air pollution data will be fetched.",
).info(
    "Get the API Key from [here](https://openweathermap.org/price)"
).done()
