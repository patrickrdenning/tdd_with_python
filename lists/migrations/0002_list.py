# Generated by Django 5.0 on 2023-12-18 08:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lists", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="List",
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
            ],
        ),
    ]
