#!/usr/bin/env python
"""
Скрипт для проверки подключения к базе данных PostgreSQL
"""
import os
import sys
import django
from pathlib import Path

# Добавляем путь к проекту
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
django.setup()

from django.db import connection
from django.core.exceptions import ImproperlyConfigured

def check_database_connection():
    """Проверяет подключение к базе данных"""
    try:
        # Проверяем подключение
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
        if result:
            print("✅ Подключение к базе данных успешно!")
            print(f"📊 База данных: {connection.settings_dict['NAME']}")
            print(f"👤 Пользователь: {connection.settings_dict['USER']}")
            print(f"🌐 Хост: {connection.settings_dict['HOST']}:{connection.settings_dict['PORT']}")
            return True
        else:
            print("❌ Ошибка: Не удалось выполнить запрос к базе данных")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка подключения к базе данных: {e}")
        print("\n🔧 Возможные решения:")
        print("1. Убедитесь, что PostgreSQL запущен")
        print("2. Проверьте настройки в shop/settings.py")
        print("3. Создайте базу данных и пользователя")
        print("4. Проверьте права доступа")
        return False

if __name__ == "__main__":
    print("🔍 Проверка подключения к базе данных...")
    success = check_database_connection()
    
    if success:
        print("\n🎉 Проект готов к работе!")
    else:
        print("\n⚠️  Требуется настройка базы данных")
        sys.exit(1)
