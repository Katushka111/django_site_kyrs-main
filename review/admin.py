from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'rating', 'product_id', 'created', 'is_approved']
    list_filter = ['rating', 'is_approved', 'created']
    search_fields = ['author_name', 'author_email', 'text']
    list_editable = ['is_approved']
    readonly_fields = ['created', 'updated']
    ordering = ['-created']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('author_name', 'author_email', 'product_id')
        }),
        ('Отзыв', {
            'fields': ('rating', 'text')
        }),
        ('Модерация', {
            'fields': ('is_approved',)
        }),
        ('Временные метки', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',)
        }),
    )
