from django.core.management.base import BaseCommand
from user.models import Achievement

class Command(BaseCommand):
    help = 'Load initial achievements data'
    
    def handle(self, *args, **options):
        achievements_data = [
            {
                'name': 'Первый шаг',
                'description': 'Зарегистрируйтесь в системе',
                'icon': '👋',
                'achievement_type': 'system',
                'points_reward': 50,
                'requirement': 1
            },
            {
                'name': 'Первая тренировка',
                'description': 'Посетите первую тренировку',
                'icon': '💪',
                'achievement_type': 'workout',
                'points_reward': 25,
                'requirement': 1
            },
            {
                'name': 'Атлет недели',
                'description': 'Посетите 5 тренировок за неделю',
                'icon': '⭐',
                'achievement_type': 'workout',
                'points_reward': 100,
                'requirement': 5
            },
            {
                'name': 'Первый заказ',
                'description': 'Закажите первую услугу',
                'icon': '🎯',
                'achievement_type': 'service',
                'points_reward': 30,
                'requirement': 1
            },
            {
                'name': 'Постоянный клиент',
                'description': 'Закажите 10 услуг',
                'icon': '🎖️',
                'achievement_type': 'service',
                'points_reward': 150,
                'requirement': 10
            },
        ]
        
        for data in achievements_data:
            achievement, created = Achievement.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created achievement: {data["name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Achievement already exists: {data["name"]}'))