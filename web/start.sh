#!/bin/bash
# start.sh


# Применение миграций
python manage.py migrate


# Запуск Gunicorn
exec gunicorn --bind 0.0.0.0:8000 web.wsgi:application