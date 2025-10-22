#!/bin/bash
# Скрипт для запуска PostgreSQL сервера

echo "Запуск PostgreSQL сервера..."
/usr/lib/postgresql/17/bin/pg_ctl -D ~/postgres_data -l ~/postgres_data/logfile start

echo "PostgreSQL сервер запущен на порту 5433"
echo "Для остановки используйте: /usr/lib/postgresql/17/bin/pg_ctl -D ~/postgres_data stop"
