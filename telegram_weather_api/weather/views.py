from datetime import timedelta

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework.views import APIView

from weather.models import Weather
from weather.serializers import WeatherSerializer, CitySerializer

from weather.selectors import weather_get_by_city_name, city_get_by_name, city_get_by_first_char, cache_get

from weather.services import cache_set, fetch_weather_data, weather_create, weather_update


class CityGetApiViewByFirstChar(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        char = request.query_params.get("char")
        if not char:
            return Response({"char": "Char not provided"}, status=status.HTTP_400_BAD_REQUEST)
        char = char.upper()
        cache_key = f"city_char_{char}"

        cached_data = cache_get(cache_key)

        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        else:
            cities = city_get_by_first_char(first_char=char)
            cache_set(cache_key, CitySerializer(cities, many=True).data, timeout=timedelta(minutes=30).seconds)
            return Response(CitySerializer(cities, many=True).data, status=status.HTTP_200_OK)


class WeatherGetApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        city_name = request.query_params.get("city")
        if not city_name:
            return Response({"city_name": "City name not provided"}, status=status.HTTP_400_BAD_REQUEST)
        city_name = city_name.title()
        cache_key = f"weather_{city_name}"

        cached_data = cache_get(cache_key)

        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        try:
            weather_get_by_city_name(city_name)
            temp, pressure, wind_speed = fetch_weather_data(city_name)
            weather_update(city_name, temp, pressure, wind_speed)
            weather_data = weather_get_by_city_name(city_name)
        except Weather.DoesNotExist:
            temp, pressure, wind_speed = fetch_weather_data(city_name)
            city = city_get_by_name(city_name)
            weather_create(city, temp, pressure, wind_speed)
            weather_data = weather_get_by_city_name(city_name)

        cache_set(cache_key, WeatherSerializer(weather_data).data, timeout=timedelta(minutes=30).seconds)

        return Response(WeatherSerializer(weather_data).data, status=status.HTTP_200_OK)




