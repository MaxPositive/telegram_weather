import logging
import os
from time import sleep

import httpx
from dotenv import load_dotenv

from telethon import TelegramClient, events, Button

load_dotenv()

logging.basicConfig(format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING)

logger = logging.getLogger(__name__)


TELEGRAM_API_ID = int(os.getenv("TELEGRAM_API_ID"))

TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

start_text = """
Привет! Я бот {}
Это бот для получения погоды по всем российским городам!
У меня есть несколько инструментов для этого:
‣ получить список всех городов
‣ получить информацию о погоде по указанному городу

"""

bot = TelegramClient("sessions/session_master", api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH).start(
    bot_token=TELEGRAM_BOT_TOKEN
)


async def delete_weather_state(event, time):
    """
    Coroutine to delete the state after the user get information about weather
    :param event: event object
    :param time: time in which to display first message
    :return: event on_start
    """
    delattr(bot, "sender_id_in_progress_weather")
    sleep(time)
    await on_start(event)


async def delete_city_state(event, time):
    """
    Coroutine to delete the state after the user get information about city
    :param event: event object
    :param time: time in which to display first message
    :return: event on_start
    """
    delattr(bot, "sender_id_in_progress_city")
    sleep(time)
    await on_start(event)


async def fetch_weather_data_from_api(city_name):
    """
    Coroutine to fetch weather data from api
    :param city_name: name of the city to get weather data from api
    :return: json object with weather data
    """
    url = f"http://localhost:8000/weather?city={city_name}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()


async def fetch_city_data_from_api(first_char):
    """
    Coroutine to fetch city data from api
    :param first_char: first character that city can have
    :return: many json objects with city name data
    """
    url = f"http://localhost:8000/cities?char={str(first_char)}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()


@bot.on(events.NewMessage(pattern="/start"))
async def on_start(event):
    """
    Coroutine that shows first message to user
    """
    formatted_start_text = start_text.format("Погодник", data=b"get_weather")

    get_weather_button = Button.inline("Получить погоду на сегодня")
    get_city_button = Button.inline("Получить список городов на букву")

    await event.reply(formatted_start_text, buttons=[get_weather_button, get_city_button])


@bot.on(events.CallbackQuery(pattern="Получить погоду на сегодня"))
async def weather_callback_handler(event):
    """
    Callback after user click to get weather
    """
    await event.reply("Напиши имя города, в котором ты хочешь получить погоду:")
    sender = await event.get_sender()

    bot.sender_id_in_progress_weather = sender.id


@bot.on(events.CallbackQuery(pattern="Получить список городов на букву"))
async def city_callback_handler(event):
    """
    Callback after user click to get all cities which start of some character
    """
    await event.reply("Напиши на какую букву выдать тебе города?")
    sender = await event.get_sender()
    bot.sender_id_in_progress_city = sender.id


@bot.on(events.NewMessage())
async def handle_first_char_input(event):
    """
    Event to handle the get the city of the first character
    :return: message with the list of all cities
    """
    if not hasattr(bot, "sender_id_in_progress_city"):
        return None
    try:
        char = event.message.text.upper().strip()
        cities = await fetch_city_data_from_api(char)
        city_names = [city["name"] for city in cities]
        message = f"Список всех городов на букву {char}:\n{', '.join(city_names)}"
        await event.reply(message)
        await delete_city_state(event, 1)

    except Exception as e:
        logger.warning(f"There was an error: {str(e)}")
        await event.reply("Произошла непредвиденная ошибка. Повторите попытку или подождите некоторое время!")
        await delete_city_state(event, 2)


@bot.on(events.NewMessage())
async def handle_city_input(event):
    """
    Event to handle the get the weather of the city
    :return: Weather data
    """
    if not hasattr(bot, "sender_id_in_progress_weather"):
        return
    city_name = event.message.text.strip()
    try:
        weather_data = await fetch_weather_data_from_api(city_name)
        if not weather_data:
            message = f"Не удалось получить погоду для города - {city_name.title()}"
            await event.reply(message)
            await delete_weather_state(event, 2)
        city = weather_data.get("city")
        temp = weather_data.get("temperature")
        pressure = weather_data.get("pressure")
        wind_speed = weather_data.get("wind_speed")
        if city is None or temp is None or pressure is None or wind_speed is None:
            message = f"Не удалось получить погоду для города - {city_name.title()}"
        else:
            message = f"Город: {city_name}\nТемпература: {temp}\nАтмосферное давление: {pressure}\nСкорость ветра: {wind_speed}"
        await event.reply(message)
        await delete_weather_state(event, 1)
    except Exception as e:
        logger.warning(f"There was an error: {str(e)}")
        await event.reply("Произошла непредвиденная ошибка. Повторите попытку или подождите некоторое время!")
        await delete_weather_state(event, 2)


if __name__ == "__main__":
    print("Bot is ready to accept requests")
    bot.run_until_disconnected()
