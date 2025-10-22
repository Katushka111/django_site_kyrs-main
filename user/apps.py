from django.apps import AppConfig

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'
    
    def ready(self):
        # Импортируем сигналы только после загрузки приложения
        try:
            import user.signals
        except ImportError:
            # Игнорируем ошибку импорта при миграциях
            pass