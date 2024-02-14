from django.core.cache import cache

from rest_framework.generics import get_object_or_404

from weather.models import Weather, City


def city_get_by_first_char(first_char: str):
    """
    Get all cities that are starting from given first char
    :param first_char: the first char of city names
    :return: city instance
    """
    cities = City.objects.filter(name__startswith=first_char).all()
    return cities


def weather_get_by_city_name(city_name):
    """
    Get weather data by city name.
    :param city_name: the name of the city
    :return: Weather instance
    """
    weather = Weather.objects.get(city__name=city_name)
    return weather


def city_get_longitude_and_latitude(city_name):
    """
    Get longitude and latitude of the city.
    :param city_name: the name of the city
    :return: longitude and latitude of the city
    """
    city = get_object_or_404(City, name=city_name)
    return city.latitude, city.longitude


def city_get_by_name(city_name):
    """
    Get city by name.
    :param city_name: the name of the city
    :return: city object
    """
    city = get_object_or_404(City, name=city_name)
    return city


def cache_get(key):
    """
    Get data from cache by key
    :param key: the key of the data
    :return: Data
    """
    return cache.get(key)