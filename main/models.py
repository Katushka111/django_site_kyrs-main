from django.db import models
from django.urls import reverse



class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("main:product_list_by_category", args=[self.slug])
    

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('name',)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("main:product_detail", args=[self.id, self.slug])

    






class Service(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название услуги')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    trainer_name = models.CharField(max_length=100, verbose_name='ФИО тренера')
    trainer_photo = models.ImageField(upload_to='trainers/%Y/%m/%d', blank=True, verbose_name='Фото тренера')
    event_time = models.DateTimeField(verbose_name='Время мероприятия')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость')
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='services/%Y/%m/%d', blank=True, verbose_name='Фото услуги')
    available = models.BooleanField(default=True, verbose_name='Доступно')
    capacity = models.PositiveIntegerField(default=10, verbose_name='Количество мест')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('event_time',)
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("main:service_detail", args=[self.id, self.slug])

    @property
    def booked_count(self) -> int:
        return self.bookings.count()

    @property
    def seats_left(self) -> int:
        remaining = self.capacity - self.booked_count
        return remaining if remaining > 0 else 0

    @property
    def is_full(self) -> bool:
        return self.booked_count >= self.capacity


class UserService(models.Model):
    user = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='booked_services')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Запись на услугу'
        verbose_name_plural = 'Записи на услуги'
        unique_together = ('user', 'service')
    
    def __str__(self):
        return f"{self.user.first_name} - {self.service.name}"
