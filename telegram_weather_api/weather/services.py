import requests

from django.conf import settings

from django.core.cache import cache

from config.exceptions import ApplicationError
from weather.models import Weather
from weather.selectors import city_get_longitude_and_latitude, weather_get_by_city_name


def weather_create(city, temp, pressure, wind_speed):
    """
    Create a weather instance
    :param city: city instance
    :param temp: temperature
    :param pressure: pressure
    :param wind_speed: wind speed
    :return: weather instance
    """
    return Weather.objects.create(city=city, temperature=temp, pressure=pressure, wind_speed=wind_speed)


def weather_update(city_name, temp, pressure, wind_speed):
    weather = weather_get_by_city_name(city_name)
    weather.temperature = temp
    weather.pressure = pressure
    weather.wind_speed = wind_speed
    weather.save()


def fetch_weather_data(city_name):
    yandex_api_key = settings.YANDEX_API_KEY
    longitude, latitude = city_get_longitude_and_latitude(city_name)
    yandex_api_url_v2 = f"https://api.weather.yandex.ru/v2/forecast?lat={latitude}&lon={longitude}&lang=ru_RU"
    headers = {"X-Yandex-API-Key": yandex_api_key}
    response = requests.get(yandex_api_url_v2, headers=headers)
    weather_data = response.json().get("fact", None)
    if weather_data:
        temp = weather_data["temp"]
        pressure = weather_data["pressure_mm"]
        wind_speed = weather_data["wind_speed"]
        return temp, pressure, wind_speed
    else:
        raise ApplicationError("Some error occurred then making api request")


def cache_set(key, data, timeout=None):
    """
    Set data in cache
    :param key: key of the data
    :param data: data to cache
    :param timeout: timeout in seconds
    :return:
    """
    return cache.set(key, data, timeout=timeout)

