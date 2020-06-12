# Generated by Django 3.0.6 on 2020-05-19 13:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("healthier", "0002_auto_20200519_1042"),
    ]

    operations = [
        migrations.AddField(
            model_name="food_item",
            name="favoris",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(name="User",),
    ]
