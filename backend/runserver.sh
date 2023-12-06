#!/bin/sh
python manage.py collectstatic --no-input
python manage.py migrate --no-input
python manage.py create_admin
celery -A tasks worker -l info -E -D
celery -A tasks beat --detach -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
gunicorn config.wsgi:application --bind 0:8000 --workers 2 --timeout 120