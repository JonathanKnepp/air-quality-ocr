# Generated by Django 5.0.4 on 2024-04-16 20:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aqi', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aqientry',
            old_name='capture_datetime',
            new_name='capture_time',
        ),
    ]
