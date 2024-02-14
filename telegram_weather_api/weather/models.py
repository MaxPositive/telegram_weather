from django.db import models


class City(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

class Weather(models.Model):
    id = models.BigAutoField(primary_key=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temperature = models.FloatField()
    pressure = models.FloatField()
    wind_speed = models.FloatField()

    @property
    def get_city_name(self):
        return self.city.name

    @property
    def get_temperature(self):
        return f"{self.temperature}°C"

    @property
    def get_pressure(self):
        return f"{self.pressure} мм.рт.ст"

    @property
    def get_wind_speed(self):
        return f"{self.wind_speed} м/c"

    def __str__(self):
        return f"{self.get_city_name} {self.get_temperature} {self.get_pressure} {self.get_wind_speed}"

