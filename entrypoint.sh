#!/bin/sh
set -e

# Run migrations and ensure superuser credentials exist on every container boot
python manage.py migrate --noinput
python ensure_admin.py

exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 0 config.wsgi:application
