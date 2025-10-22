from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.html import strip_tags
from django.utils import timezone
from datetime import timedelta


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            return ValueError('The email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self.create_user(email, first_name, last_name, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=66)
    first_name = models.CharField(max_length=66)
    last_name = models.CharField(max_length=66)
    is_trener = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, blank=True, null=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    experience_points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    
    def clean(self):
        for field in ['phone']:
            value = getattr(self, field)
            if value:
                setattr(self, field, strip_tags(value))
    
    def add_experience(self, points):
        """Добавляет опыт пользователю и проверяет повышение уровня"""
        self.experience_points += points
        self.check_level_up()
        self.save()
    
    def check_level_up(self):
        """Проверяет, нужно ли повысить уровень пользователя"""
        points_needed = self.level * 100  # Например, 100 очков на уровень
        if self.experience_points >= points_needed:
            self.level += 1
            # Создаем уведомление о повышении уровня
            Notifications.objects.create(
                user=self,
                message=f"🎉 Поздравляем! Вы достигли {self.level} уровня!"
            )
            return True
        return False
    
    def get_next_level_points(self):
        """Возвращает количество очков до следующего уровня"""
        return (self.level * 100) - self.experience_points
    
    def get_total_progress_percentage(self):
        """Возвращает общий процент выполнения всех целей"""
        progress_entries = UserProgress.objects.filter(user=self, is_completed=True)
        if not progress_entries.exists():
            return 0
        return int((progress_entries.count() / UserProgress.objects.filter(user=self).count()) * 100)


class ProgressCategory(models.Model):
    CATEGORY_TYPES = [
        ('fitness', '🏋️ Фитнес'),
        ('nutrition', '🥗 Питание'),
        ('health', '💊 Здоровье'),
        ('lifestyle', '🌿 Образ жизни'),
        ('personal', '🎯 Личные цели'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Название категории")
    icon = models.CharField(max_length=20, default="⭐", verbose_name="Иконка")
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPES, verbose_name="Тип категории")
    description = models.TextField(blank=True, verbose_name="Описание")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Категория прогресса"
        verbose_name_plural = "Категории прогресса"
        ordering = ['category_type', 'name']

    def __str__(self):
        return f"{self.icon} {self.name}"


class UserProgress(models.Model):
    PROGRESS_STATUS = [
        ('not_started', 'Не начато'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершено'),
        ('failed', 'Не удалось'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='progress_entries')
    category = models.ForeignKey(ProgressCategory, on_delete=models.CASCADE, verbose_name="Категория")
    title = models.CharField(max_length=200, verbose_name="Название цели")
    description = models.TextField(blank=True, verbose_name="Описание цели")
    target_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Целевое значение")
    current_value = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Текущее значение")
    unit = models.CharField(max_length=20, default="раз", verbose_name="Единица измерения")
    status = models.CharField(max_length=20, choices=PROGRESS_STATUS, default='not_started', verbose_name="Статус")
    priority = models.IntegerField(default=1, choices=[(1, 'Низкий'), (2, 'Средний'), (3, 'Высокий')], verbose_name="Приоритет")
    start_date = models.DateField(default=timezone.now, verbose_name="Дата начала")
    end_date = models.DateField(null=True, blank=True, verbose_name="Дата завершения")
    is_completed = models.BooleanField(default=False, verbose_name="Завершено")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата завершения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Прогресс пользователя"
        verbose_name_plural = "Прогресс пользователей"
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.title}"
    
    def save(self, *args, **kwargs):
        # Автоматически обновляем статус при изменении значений
        if self.current_value >= self.target_value and not self.is_completed:
            self.status = 'completed'
            self.is_completed = True
            self.completed_at = timezone.now()
            
            # Награждаем пользователя опытом
            experience_points = int(self.target_value * self.priority)
            self.user.add_experience(experience_points)
            
            # Создаем уведомление о завершении цели
            Notifications.objects.create(
                user=self.user,
                message=f"🎯 Цель достигнута: {self.title}! +{experience_points} опыта"
            )
        
        elif self.current_value > 0 and self.status == 'not_started':
            self.status = 'in_progress'
        
        super().save(*args, **kwargs)
    
    @property
    def progress_percentage(self):
        """Возвращает процент выполнения цели"""
        if self.target_value == 0:
            return 0
        return min(100, int((float(self.current_value) / float(self.target_value)) * 100))
    
    @property
    def days_remaining(self):
        """Возвращает количество оставшихся дней"""
        if self.end_date and not self.is_completed:
            remaining = (self.end_date - timezone.now().date()).days
            return max(0, remaining)
        return None
    
    @property
    def is_overdue(self):
        """Проверяет, просрочена ли цель"""
        if self.end_date and not self.is_completed:
            return timezone.now().date() > self.end_date
        return False


class ProgressUpdate(models.Model):
    progress = models.ForeignKey(UserProgress, on_delete=models.CASCADE, related_name='updates')
    value_added = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Добавленное значение")
    notes = models.TextField(blank=True, verbose_name="Заметки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Обновление прогресса"
        verbose_name_plural = "Обновления прогресса"
        ordering = ['-created_at']

    def __str__(self):
        return f"Обновление {self.progress.title} - +{self.value_added}"


class Achievement(models.Model):
    ACHIEVEMENT_TYPES = [
        ('workout', 'Тренировки'),
        ('service', 'Услуги'),
        ('shopping', 'Покупки'),
        ('social', 'Социальные'),
        ('system', 'Системные'),
        ('progress', 'Прогресс'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    icon = models.CharField(max_length=50, default="🏆", verbose_name="Иконка")
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPES, verbose_name="Тип ачивки")
    points_reward = models.IntegerField(default=10, verbose_name="Награда в очках")
    requirement = models.IntegerField(default=1, verbose_name="Требование")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Ачивка"
        verbose_name_plural = "Ачивки"
        ordering = ['achievement_type', 'requirement']

    def __str__(self):
        return f"{self.icon} {self.name}"


class UserAchievement(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0, verbose_name="Прогресс")
    is_unlocked = models.BooleanField(default=False, verbose_name="Разблокирована")
    unlocked_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата получения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Ачивка пользователя"
        verbose_name_plural = "Ачивки пользователей"
        unique_together = ['user', 'achievement']
        ordering = ['-unlocked_at', '-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.achievement.name}"
    
    def update_progress(self, amount=1):
        """Обновляет прогресс ачивки"""
        if not self.is_unlocked:
            self.progress += amount
            if self.progress >= self.achievement.requirement:
                self.unlock()
            self.save()
    
    def unlock(self):
        """Разблокирует ачивку и награждает пользователя"""
        if not self.is_unlocked:
            self.is_unlocked = True
            self.unlocked_at = timezone.now()
            self.user.add_experience(self.achievement.points_reward)
            
            # Создаем уведомление о получении ачивки
            Notifications.objects.create(
                user=self.user,
                message=f"🎖️ Получена ачивка: {self.achievement.name}! +{self.achievement.points_reward} опыта"
            )
    
    @property
    def progress_percentage(self):
        """Возвращает процент выполнения ачивки"""
        if self.achievement.requirement == 0:
            return 100
        return min(100, int((self.progress / self.achievement.requirement) * 100))


class Notifications(models.Model):
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Уведомление для {self.user}: {self.message[:50]}..."
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.deleted_at:
            self.deleted_at = timezone.now() + timedelta(days=1)
        super().save(*args, **kwargs)
    
    @property
    def is_expired(self):
        return timezone.now() >= self.deleted_at if self.deleted_at else False