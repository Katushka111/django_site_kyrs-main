from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL")
    content = models.TextField(verbose_name="Содержание")
    excerpt = models.TextField(max_length=300, blank=True, verbose_name="Краткое описание")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', verbose_name="Автор")
    image = models.ImageField(upload_to='articles/%Y/%m/%d/', blank=True, null=True, verbose_name="Изображение")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="Статус")
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    
    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-created']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('articles:article_detail', kwargs={'slug': self.slug})
    
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])