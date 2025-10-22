# Миграция с SQLite на PostgreSQL

## Выполненные шаги

1. ✅ Установлен PostgreSQL и psycopg2-binary
2. ✅ Создана локальная база данных PostgreSQL на порту 5433
3. ✅ Обновлены настройки Django для использования PostgreSQL
4. ✅ Применены все миграции
5. ✅ Создан файл .env с SECRET_KEY
6. ✅ Созданы скрипты для удобного запуска

## Настройки базы данных

- **Хост**: localhost
- **Порт**: 5433
- **База данных**: django_site_kyrs
- **Пользователь**: anzherus
- **Пароль**: 1029384756SetKvazar

## Запуск проекта

### Автоматический запуск (рекомендуется)
```bash
./run_django.sh
```

### Ручной запуск
1. Запустить PostgreSQL:
```bash
./start_postgres.sh
```

2. Запустить Django:
```bash
source venv/bin/activate
python manage.py runserver 127.0.0.1:8000
```

## Остановка сервисов

### Остановить Django
```bash
pkill -f "python manage.py runserver"
```

### Остановить PostgreSQL
```bash
/usr/lib/postgresql/17/bin/pg_ctl -D ~/postgres_data stop
```

## Проверка подключения к базе данных

```bash
psql -h localhost -p 5433 -U anzherus -d django_site_kyrs -c "SELECT 1;"
```

## Файлы конфигурации

- `shop/settings.py` - настройки Django с PostgreSQL
- `.env` - переменные окружения (SECRET_KEY)
- `requirements.txt` - зависимости проекта
- `~/postgres_data/` - данные PostgreSQL
