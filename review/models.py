from django.db import models
from django.urls import reverse
from django.conf import settings,Settings

class Review(models.Model):
    class Stars(models.IntegerChoices):
        ONE = 1, '⭐'
        TWO = 2, '⭐⭐'
        THREE = 3, '⭐⭐⭐'
        FOUR = 4, '⭐⭐⭐⭐'
        FIVE = 5, '⭐⭐⭐⭐⭐'
    
    # Связь с товаром будет добавлена через миграцию
    product_id = models.PositiveIntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(choices=Stars.choices, default=5)
    text = models.TextField(max_length=1000, help_text="Ваш отзыв о товаре")
    author_name = models.CharField(max_length=100, help_text="Ваше имя")
    author_email = models.EmailField(help_text="Ваш email")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=True, help_text="Одобрен ли отзыв для публикации")

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
    
    def __str__(self):
        return f"{self.author_name} - {self.get_rating_display()} - {self.text[:50]}..."
    
    def get_absolute_url(self):
        return reverse('review:review_detail', args=[self.id])