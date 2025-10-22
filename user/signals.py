from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import CustomUser, Achievement, UserAchievement
from django.utils import timezone

@receiver(post_save, sender=CustomUser)
def create_initial_achievements(sender, instance, created, **kwargs):
    """
    Создает начальные ачивки для нового пользователя
    """
    if created:
        try:
            # Создаем или получаем ачивку за регистрацию
            registration_achievement, created_ach = Achievement.objects.get_or_create(
                name="Первый шаг",
                defaults={
                    'description': "Зарегистрируйтесь в системе",
                    'icon': "👋",
                    'achievement_type': 'system',
                    'points_reward': 50,
                    'requirement': 1,
                    'is_active': True
                }
            )
            
            # Создаем запись ачивки пользователя
            UserAchievement.objects.create(
                user=instance,
                achievement=registration_achievement,
                progress=1,
                is_unlocked=True,
                unlocked_at=instance.date_joined
            )
            
            # Добавляем опыт за регистрацию
            instance.add_experience(registration_achievement.points_reward)
            
        except Exception as e:
            # Логируем ошибку, но не прерываем процесс
            print(f"Error creating initial achievements: {e}")

def update_user_achievement(user, achievement_name, progress_amount=1):
    """
    Универсальная функция для обновления прогресса ачивки пользователя
    """
    try:
        achievement = Achievement.objects.get(
            name=achievement_name, 
            is_active=True
        )
        
        user_achievement, created = UserAchievement.objects.get_or_create(
            user=user,
            achievement=achievement,
            defaults={'progress': progress_amount}
        )
        
        if not user_achievement.is_unlocked:
            if created:
                # Если создана новая запись, проверяем сразу разблокировку
                if user_achievement.progress >= achievement.requirement:
                    user_achievement.unlock()
                else:
                    user_achievement.save()
            else:
                # Обновляем существующую запись
                user_achievement.update_progress(progress_amount)
                
    except Achievement.DoesNotExist:
        # Ачивка не найдена - это нормально, просто игнорируем
        pass
    except Exception as e:
        print(f"Error updating achievement {achievement_name}: {e}")

# Примеры функций для различных событий (можно вызывать из других приложений)
def on_user_completed_workout(user, workout_type):
    """Вызывается когда пользователь завершил тренировку"""
    update_user_achievement(user, "Первая тренировка")
    update_user_achievement(user, "Атлет недели", 1)

def on_user_booked_service(user):
    """Вызывается когда пользователь записался на услугу"""
    update_user_achievement(user, "Первый заказ")
    update_user_achievement(user, "Постоянный клиент", 1)

def on_user_made_purchase(user, amount):
    """Вызывается когда пользователь совершил покупку"""
    update_user_achievement(user, "Первая покупка")
    if amount > 100:
        update_user_achievement(user, "Крупный покупатель")