from django.core.management.base import BaseCommand, CommandError
from aqi.classes import AirQualityOCR, VideoCapture
from django.conf import settings
from aqi.models import AQIEntry
from datetime import datetime
import os


class Command(BaseCommand):
    help = "Capture an image for OCR"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        # Capture an image from the camera
        cam = VideoCapture(0)
        cam.capture_image(f'images/queue/capture_{datetime.now().strftime("%Y%m%d%H%M%S")}.png')
