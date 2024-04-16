from django.core.management.base import BaseCommand, CommandError
from aqi.classes import AirQualityOCR, VideoCapture
from django.conf import settings
from aqi.models import AQIEntry
import os


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        for img_path in AirQualityOCR.queue_images():
            # Get the AQI data points from our image
            ocr = AirQualityOCR(img_path)
            data_points = ocr.get_data_points()

            # Archive the crops and images
            ocr.archive()

            # Create an entry in the database
            a = AQIEntry(**data_points)
            a.capture_time = ocr.get_capture_time()
            a.save()
