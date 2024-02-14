from rest_framework import serializers
from weather.models import Weather, City


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ["id", "city", 'temperature', 'pressure', 'wind_speed']

    def to_representation(self, instance):
        data = super(WeatherSerializer, self).to_representation(instance)
        data["city"] = instance.get_city_name
        data['temperature'] = instance.get_temperature
        data['pressure'] = instance.get_pressure
        data['wind_speed'] = instance.get_wind_speed
        return data


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["name"]