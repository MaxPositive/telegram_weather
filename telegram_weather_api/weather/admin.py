from django.contrib import admin

from weather.models import Weather, City


@admin.register(Weather)
class WeatherAdmin(admin.ModelAdmin):
    list_display = ("id", "city", 'temperature', "pressure", "wind_speed")


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "latitude", "longitude")
