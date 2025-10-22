from django.contrib import admin
from .models import Category, Product, Service, UserService

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug':('name',)}
    search_fields = ['name', 'description']
    readonly_fields = ['created', 'updated']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Изображение и цена', {
            'fields': ('image', 'price', 'available')
        }),
        ('Метаданные', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'trainer_name', 'event_time', 'price', 'available', 'created']
    list_filter = ['available', 'created', 'event_time']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug':('name',)}
    search_fields = ['name', 'trainer_name', 'description']
    readonly_fields = ['created', 'updated']
    date_hierarchy = 'event_time'

@admin.register(UserService)
class UserServiceAdmin(admin.ModelAdmin):
    list_display = ['user', 'service', 'booking_date', 'is_confirmed']
    list_filter = ['is_confirmed', 'booking_date']
    search_fields = ['user__first_name', 'user__last_name', 'service__name']
    readonly_fields = ['booking_date']