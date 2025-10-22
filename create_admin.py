#!/usr/bin/env python
"""
Простой скрипт для создания суперпользователя с предустановленными данными
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
django.setup()

from django.contrib.auth import get_user_model

def create_admin():
    User = get_user_model()
    
    # Данные для создания суперпользователя
    username = "admin_user"
    email = "admin@django.com"
    password = "admin123456"
    
    print("=== Создание суперпользователя Django ===")
    print(f"Имя пользователя: {username}")
    print(f"Email: {email}")
    print(f"Пароль: {password}")
    print()
    
    # Проверка существования пользователя
    if User.objects.filter(username=username).exists():
        print(f"Пользователь '{username}' уже существует!")
        return
    
    # Создание суперпользователя
    try:
        user = User.objects.create_superuser(
            email=email,
            first_name="Admin",
            last_name="User",
            password=password,
            username=username
        )
        print("✅ Суперпользователь успешно создан!")
        print()
        print("Данные для входа в админку:")
        print(f"   URL: http://127.0.0.1:8000/admin/")
        print(f"   Имя пользователя: {username}")
        print(f"   Пароль: {password}")
        
    except Exception as e:
        print(f"Ошибка при создании пользователя: {e}")

if __name__ == "__main__":
    create_admin()
