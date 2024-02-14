from django.urls import path

from weather.views import WeatherGetApiView, CityGetApiViewByFirstChar

urlpatterns = [
    path("weather", WeatherGetApiView.as_view(), name="weather-get"),
    path("cities", CityGetApiViewByFirstChar.as_view(), name="city-get-all")
]