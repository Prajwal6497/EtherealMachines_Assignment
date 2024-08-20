# Generated by Django 5.1 on 2024-08-20 03:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="EtherealMachine",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("feedrate", models.FloatField()),
                ("max_acceleration", models.FloatField()),
                ("max_velocity", models.FloatField()),
                ("acceleration", models.FloatField()),
                ("angular_units", models.FloatField()),
                ("velocity", models.FloatField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="AxisData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("axis", models.CharField(max_length=1)),
                ("actual_position", models.FloatField()),
                ("distance_to_go", models.FloatField()),
                ("tool_offset", models.FloatField()),
                ("homed", models.BooleanField(default=False)),
                (
                    "machine",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="axis_data",
                        to="etherealmachines.etherealmachine",
                    ),
                ),
            ],
        ),
    ]