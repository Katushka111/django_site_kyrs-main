from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserUpdatedForm, UserProgressForm, ProgressUpdateForm
from .models import CustomUser, Notifications, UserAchievement, UserProgress, ProgressCategory, ProgressUpdate
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('user:profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('user:profile')
    else:
        form = CustomUserLoginForm()
    return render(request, 'user/login.html', {'form': form})


@login_required
def profile_view(request):
    # Получаем активные уведомления пользователя
    notifications = Notifications.objects.filter(
        user=request.user,
        is_active=True
    ).order_by('-created_at')
    
    # Получаем ачивки пользователя
    user_achievements = UserAchievement.objects.filter(
        user=request.user
    ).select_related('achievement').order_by('-unlocked_at', '-created_at')
    
    # Получаем прогресс пользователя
    user_progress = UserProgress.objects.filter(
        user=request.user
    ).select_related('category').order_by('-priority', '-created_at')
    
    # Получаем категории для формы
    categories = ProgressCategory.objects.filter(is_active=True)
    
    # Автоматически помечаем как неактивные просроченные уведомления
    expired_notifications = Notifications.objects.filter(
        user=request.user,
        deleted_at__lte=timezone.now(),
        is_active=True
    )
    expired_notifications.update(is_active=False)
    
    return render(request, 'user/profile.html', {
        'user': request.user,
        'notifications': notifications,
        'achievements': user_achievements,
        'progress_entries': user_progress,
        'progress_categories': categories,
        'progress_form': UserProgressForm(),
        'update_form': ProgressUpdateForm()
    })


@login_required
def account_ditail(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, 'user/partials/account_details.html', {'user': user})


@login_required
def edit_account_ditail(request):
    form = CustomUserUpdatedForm(instance=request.user)
    return render(request, 'user/partials/edit_account_details.html', {'user': request.user, 'form': form})


@login_required
def update_account_ditail(request):
    if request.method == 'POST':
        form = CustomUserUpdatedForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.clean()
            user.save()
            return render(request, 'user/partials/account_details.html', {'user': user})
        else:
            return render(request, 'user/partials/account_details.html', {'user': request.user, 'form': form})
    return render(request, 'user/partials/account_details.html', {'user': request.user})


def logout_view(request):
    logout(request)
    return redirect('user:register')


@login_required
def delete_notification(request, notification_id):
    """Удаление уведомления"""
    if request.method == 'POST':
        try:
            notification = Notifications.objects.get(
                id=notification_id,
                user=request.user
            )
            notification.is_active = False
            notification.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('user:profile')
            
        except Notifications.DoesNotExist:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Уведомление не найдено'})
            return redirect('user:profile')
    
    return redirect('user:profile')


@login_required
def add_progress(request):
    """Добавление новой цели прогресса"""
    if request.method == 'POST':
        form = UserProgressForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.user = request.user
            progress.save()
            messages.success(request, 'Цель успешно добавлена!')
            return redirect('user:profile')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    return redirect('user:profile')


@login_required
def update_progress(request, progress_id):
    """Обновление прогресса цели"""
    progress = get_object_or_404(UserProgress, id=progress_id, user=request.user)
    
    if request.method == 'POST':
        form = ProgressUpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.progress = progress
            
            # Обновляем текущее значение прогресса
            progress.current_value += update.value_added
            progress.save()
            
            update.save()
            messages.success(request, f'Прогресс обновлен: +{update.value_added}')
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'current_value': float(progress.current_value),
                    'progress_percentage': progress.progress_percentage
                })
            
        else:
            messages.error(request, 'Ошибка при обновлении прогресса.')
    
    return redirect('user:profile')


@login_required
def delete_progress(request, progress_id):
    """Удаление цели прогресса"""
    progress = get_object_or_404(UserProgress, id=progress_id, user=request.user)
    
    if request.method == 'POST':
        progress.delete()
        messages.success(request, 'Цель удалена.')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
    
    return redirect('user:profile')


@login_required
def complete_progress(request, progress_id):
    """Завершение цели прогресса"""
    progress = get_object_or_404(UserProgress, id=progress_id, user=request.user)
    
    if request.method == 'POST':
        progress.current_value = progress.target_value
        progress.save()
        messages.success(request, 'Цель завершена!')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
    
    return redirect('user:profile')