#!/bin/bash

# Handle database migrations and static files if necessary
echo "============================="
echo "Migrating database and handling static files"
echo "============================="
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

# Start RabbitMQ broker (Port 5672)
echo "============================="
echo "Starting RabbitMQ"
echo "============================="
bash /usr/sbin/rabbitmq-server &

# Start Celery Beat for periodic tasks
echo "============================="
echo "Starting celery beat (for periodic tasks)"
echo "============================="
celery -A app beat --scheduler django_celery_beat.schedulers:DatabaseScheduler &

# Start celery worker with threads pool
echo "============================="
echo "Starting celery (for background tasks)"
echo "============================="
celery -A app worker --pool threads &

# Start Flower (Port 5555) for monitoring and debugging Celery tasks
# Note: Basic Auth in Nginx (cacm:c986hDPtuWkaSVQb)
echo "============================="
echo "Starting celery flower (for web-monitoring tasks)"
echo "============================="
celery flower --url_prefix=flower &

# Use gunicorn to serve our Django app
gunicorn --config gunicorn-cfg.py app.wsgi --reload