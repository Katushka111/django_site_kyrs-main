from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    
    path('products/', views.product_list, name='all_products'),
    path('category/<slug:category_slug>/',views.product_list,
         name='product_list_by_category'),
    path('product/<int:id>/<slug:slug>',views.product_detail,name='product_detail'),
    path('', views.service_list, name='service_list'),
    path('service/<int:id>/<slug:slug>', views.service_detail, name='service_detail'),
    path('service/<int:service_id>/book/', views.book_service, name='book_service'),
]
