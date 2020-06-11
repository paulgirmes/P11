# Generated by Django 3.0.6 on 2020-05-21 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthier', '0007_auto_20200521_1334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food_item',
            name='energy_kcal_100gr',
        ),
        migrations.AddField(
            model_name='food_item',
            name='energy_100g',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]