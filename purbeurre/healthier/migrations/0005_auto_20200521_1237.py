# Generated by Django 3.0.6 on 2020-05-21 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthier', '0004_auto_20200521_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food_item',
            name='id_open_food_facts',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
