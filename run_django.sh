#!/bin/bash
# Скрипт для запуска Django с PostgreSQL

echo "Запуск PostgreSQL сервера..."
/usr/lib/postgresql/17/bin/pg_ctl -D ~/postgres_data -l ~/postgres_data/logfile start

echo "Ожидание запуска PostgreSQL..."
sleep 2

echo "Активация виртуального окружения и запуск Django..."
cd /home/anzherus/django_site_kyrs
source venv/bin/activate

echo "Django сервер запускается на http://127.0.0.1:8000"
python manage.py runserver 127.0.0.1:8000
