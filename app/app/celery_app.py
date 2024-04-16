from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')

app.conf.update(
    broker_url='amqp://guest:guest@localhost',
    cache_backend='django-cache',
    result_backend='django-db',
    timezone='America/New_York',
    beat_scheduler='django_celery_beat.schedulers:DatabaseScheduler',
    result_extended=True,
    task_track_started=True,
    result_expires=0,
    broker_connection_retry_on_startup=True,
)

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
