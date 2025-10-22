from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Review
from .forms import ReviewForm

def review_list(request):
    """Список всех отзывов"""
    reviews = Review.objects.filter(is_approved=True)
    
    # Пагинация
    paginator = Paginator(reviews, 10)  # 10 отзывов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'reviews': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'review/review_list.html', context)

def review_create(request, product_id=None):
    """Создание нового отзыва"""
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save()
            messages.success(request, 'Спасибо за ваш отзыв! Он будет опубликован после модерации.')
            return redirect('review:review_list')
        else:
            # Показываем ошибки валидации
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ReviewForm(initial={'product_id': product_id})
    
    context = {
        'form': form,
        'product_id': product_id,
    }
    return render(request, 'review/review_create.html', context)

def review_detail(request, review_id):
    """Детальная страница отзыва"""
    review = get_object_or_404(Review, id=review_id, is_approved=True)
    
    context = {
        'review': review,
    }
    return render(request, 'review/review_detail.html', context)
