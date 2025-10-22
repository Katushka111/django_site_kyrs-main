from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Article

def articles_list(request):
    articles = Article.objects.filter(status='published').select_related('author')
    
    # Пагинация
    paginator = Paginator(articles, 9)  # 9 статей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'articles': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'articles/list.html', context)

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, status='published')
    
    # Увеличиваем счетчик просмотров
    article.increase_views()
    
    # Получаем похожие статьи
    similar_articles = Article.objects.filter(
        status='published'
    ).exclude(id=article.id)[:4]
    
    context = {
        'article': article,
        'similar_articles': similar_articles,
    }
    return render(request, 'articles/detail.html', context)