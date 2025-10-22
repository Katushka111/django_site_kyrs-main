from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
    path('', views.review_list, name='review_list'),
    path('create/', views.review_create, name='review_create'),
    path('create/<int:product_id>/', views.review_create, name='review_create_for_product'),
    path('<int:review_id>/', views.review_detail, name='review_detail'),
]