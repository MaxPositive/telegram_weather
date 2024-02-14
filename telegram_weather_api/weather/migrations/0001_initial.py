# Generated by Django 5.0.2 on 2024-02-12 19:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="City",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255, unique=True)),
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="Weather",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("temperature", models.FloatField()),
                ("pressure", models.FloatField()),
                ("wind_speed", models.FloatField()),
                ("city", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="weather.city")),
            ],
        ),
    ]