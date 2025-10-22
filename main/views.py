from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Product, Service, UserService
from cart.forms import CartAddProductForm
from django.urls import reverse

def product_list(request,category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    category = None
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'main/product/list.html',
                  {'category':category,
                   'categories' : categories,
                   'products':products,
                   'product_list':products})  # Добавляем product_list для отображения вкладки

def product_detail(request, id, slug):
    product = get_object_or_404(Product,id=id,slug=slug,available=True)
    related_products = Product.objects.filter(category = product.category,
                                              available = True).exclude(id=product.id)[:4]
    cart_product_form = CartAddProductForm()
    products = Product.objects.filter(available=True)  # Добавляем товары для отображения вкладки
    return render(request,'main/product/detail.html',{
        'product':product,
        'related_products':related_products,
        'cart_product_form':cart_product_form,
        'product_list':products  # Добавляем product_list для отображения вкладки
    })

def service_list(request):
    services = Service.objects.filter(available=True).order_by('event_time')
    products = Product.objects.filter(available=True)  # Добавляем товары для отображения вкладки
    return render(request, 'main/service/list.html', {
        'services': services,
        'product_list': products  # Добавляем product_list для отображения вкладки
    })

def service_detail(request, id, slug):
    service = get_object_or_404(Service, id=id, slug=slug, available=True)
    related_services = Service.objects.filter(available=True).exclude(id=service.id)[:4]
    products = Product.objects.filter(available=True)  # Добавляем товары для отображения вкладки
    return render(request, 'main/service/detail.html', {
        'service': service, 
        'related_services': related_services,
        'product_list': products  # Добавляем product_list для отображения вкладки
    })

@login_required
def book_service(request, service_id):
    service = get_object_or_404(Service, id=service_id, available=True)
    
    if request.method == 'POST':
        # Проверяем, не записан ли уже пользователь на эту услугу
        booking, created = UserService.objects.get_or_create(
            user=request.user,
            service=service,
            defaults={'is_confirmed': False}
        )
        
        if created:
            messages.success(request, f'Вы успешно записались на услугу "{service.name}"!')
        else:
            messages.info(request, f'Вы уже записаны на услугу "{service.name}".')
        
        # УБРАТЬ ЯКОРЬ #booking, так как вкладок нет
        return redirect('main:service_detail', id=service.id, slug=service.slug)
    
    return render(request, 'main/service/book.html', {'service': service})