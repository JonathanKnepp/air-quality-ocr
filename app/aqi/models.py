from django.db import models
from django_extensions.db.models import TimeStampedModel


class AQIEntry(TimeStampedModel, models.Model):
    temperature = models.FloatField(null=True)
    humidity = models.FloatField(null=True)
    tvoc = models.FloatField(null=True)
    hcho = models.FloatField(null=True)
    pm2_5 = models.FloatField(null=True)
    pm10 = models.FloatField(null=True)
    co2 = models.FloatField(null=True)
    capture_time = models.DateTimeField()

    class Meta:
        verbose_name = "AQI Entry"
        verbose_name_plural = "AQI Entries"
