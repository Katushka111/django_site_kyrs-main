from django.urls import path
from django.contrib.auth import views as auth_views  # ✅ Правильный импорт
from . import views
from .forms import CustomPasswordResetForm, CustomSetPasswordForm

app_name = 'user'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('account-details/', views.account_ditail, name='account_details'),
    path('edit-account-details/', views.edit_account_ditail, name='edit_account_details'),
    path('update-account-details/', views.update_account_ditail, name='update_account_details'),
    path('logout/', views.logout_view, name='logout'),
    path('delete-notification/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    
    # URLs для прогресса
    path('add-progress/', views.add_progress, name='add_progress'),
    path('update-progress/<int:progress_id>/', views.update_progress, name='update_progress'),
    path('delete-progress/<int:progress_id>/', views.delete_progress, name='delete_progress'),
    path('complete-progress/<int:progress_id>/', views.complete_progress, name='complete_progress'),
    
    # ✅ ПРАВИЛЬНЫЕ URLs для восстановления пароля
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='user/password_reset.html',
             form_class=CustomPasswordResetForm,
             email_template_name='user/password_reset_email.html',
             subject_template_name='user/password_reset_subject.txt',
             success_url='/user/password-reset/done/'
         ), 
         name='password_reset'),
    
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='user/password_reset_done.html'
         ), 
         name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='user/password_reset_confirm.html',
             form_class=CustomSetPasswordForm,
             success_url='/user/password-reset-complete/'
         ), 
         name='password_reset_confirm'),
    
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='user/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]