from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Notifications, CustomUser, Achievement, UserAchievement, ProgressCategory, UserProgress, ProgressUpdate


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'is_trener', 'level', 'experience_points')
    list_editable = ('last_name', 'email', 'is_trener')
    list_display_links = ('first_name',)
    list_filter = ('is_trener', 'level', 'is_staff')
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(ProgressCategory)
class ProgressCategoryAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name', 'category_type', 'is_active')
    list_filter = ('category_type', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('name', 'description')


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'category', 'progress_display', 'status', 'priority', 'is_completed')
    list_filter = ('category', 'status', 'priority', 'is_completed', 'created_at')
    list_editable = ('status', 'priority')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'title')
    readonly_fields = ('created_at', 'updated_at', 'completed_at')
    
    def progress_display(self, obj):
        return f"{obj.current_value}/{obj.target_value} {obj.unit} ({obj.progress_percentage}%)"
    progress_display.short_description = 'Прогресс'


@admin.register(ProgressUpdate)
class ProgressUpdateAdmin(admin.ModelAdmin):
    list_display = ('progress', 'value_added', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('progress__title', 'notes')
    readonly_fields = ('created_at',)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name', 'achievement_type', 'points_reward', 'requirement', 'is_active')
    list_filter = ('achievement_type', 'is_active')
    list_editable = ('points_reward', 'requirement', 'is_active')
    search_fields = ('name', 'description')


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'progress_display', 'is_unlocked', 'unlocked_at')
    list_filter = ('is_unlocked', 'achievement__achievement_type')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'achievement__name')
    readonly_fields = ('unlocked_at', 'created_at')
    
    def progress_display(self, obj):
        return f"{obj.progress}/{obj.achievement.requirement}"
    progress_display.short_description = 'Прогресс'


@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ('user', 'message_preview', 'is_active', 'created_at', 'deleted_at', 'is_expired')
    list_filter = ('is_active', 'created_at', 'deleted_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'message')
    readonly_fields = ('created_at', 'deleted_at', 'is_expired')
    list_per_page = 20
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'message', 'is_active')
        }),
        ('Даты', {
            'fields': ('created_at', 'deleted_at', 'is_expired'),
            'classes': ('collapse',)
        }),
    )
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Сообщение'
    
    def is_expired(self, obj):
        return obj.is_expired
    is_expired.short_description = 'Истекло'
    is_expired.boolean = True
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')