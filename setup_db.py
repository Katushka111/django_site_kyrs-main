#!/usr/bin/env python
"""
Скрипт для настройки базы данных PostgreSQL
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

from django.core.management import execute_from_command_line

def setup_database():
    """Настраивает базу данных"""
    print("🔧 Настройка базы данных...")
    
    try:
        # Проверяем подключение
        print("1. Проверка подключения...")
        execute_from_command_line(['manage.py', 'check'])
        print("✅ Подключение к базе данных успешно!")
        
        # Применяем миграции
        print("2. Применение миграций...")
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Миграции применены успешно!")
        
        # Создаем суперпользователя (опционально)
        print("3. Создание суперпользователя...")
        print("💡 Для создания суперпользователя выполните:")
        print("   python manage.py createsuperuser")
        
        print("\n🎉 База данных настроена успешно!")
        print("🚀 Теперь вы можете запустить сервер:")
        print("   python manage.py runserver")
        
    except Exception as e:
        print(f"❌ Ошибка настройки базы данных: {e}")
        print("\n🔧 Возможные решения:")
        print("1. Убедитесь, что PostgreSQL запущен")
        print("2. Проверьте настройки в shop/settings.py")
        print("3. Создайте базу данных и пользователя")
        print("4. Проверьте права доступа")
        return False
    
    return True

if __name__ == "__main__":
    print("🛠️  Настройка базы данных Django...")
    success = setup_database()
    
    if not success:
        sys.exit(1)
