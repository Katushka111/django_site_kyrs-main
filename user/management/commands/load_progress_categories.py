from django.core.management.base import BaseCommand
from user.models import ProgressCategory

class Command(BaseCommand):
    help = 'Load initial progress categories'
    
    def handle(self, *args, **options):
        categories_data = [
            {
                'name': 'Похудение',
                'icon': '⚖️',
                'category_type': 'fitness',
                'description': 'Цели по снижению веса'
            },
            {
                'name': 'Набор массы',
                'icon': '💪',
                'category_type': 'fitness',
                'description': 'Цели по набору мышечной массы'
            },
            {
                'name': 'Кардио тренировки',
                'icon': '🏃',
                'category_type': 'fitness',
                'description': 'Цели по кардио нагрузкам'
            },
            {
                'name': 'Силовые тренировки',
                'icon': '🏋️',
                'category_type': 'fitness',
                'description': 'Цели по силовым показателям'
            },
            {
                'name': 'Правильное питание',
                'icon': '🥗',
                'category_type': 'nutrition',
                'description': 'Цели по питанию'
            },
            {
                'name': 'Питьевой режим',
                'icon': '💧',
                'category_type': 'nutrition',
                'description': 'Цели по потреблению воды'
            },
            {
                'name': 'Здоровый сон',
                'icon': '😴',
                'category_type': 'health',
                'description': 'Цели по качеству сна'
            },
            {
                'name': 'Медитация',
                'icon': '🧘',
                'category_type': 'health',
                'description': 'Цели по медитативным практикам'
            },
        ]
        
        created_count = 0
        
        for data in categories_data:
            category, created = ProgressCategory.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Создана категория: {data["name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'↻ Категория уже существует: {data["name"]}'))
        
        self.stdout.write(self.style.SUCCESS(f'\nЗагрузка завершена! Создано категорий: {created_count}'))
        