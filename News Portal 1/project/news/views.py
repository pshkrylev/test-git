from django.shortcuts import render, get_object_or_404
from .models import Post


def news_list(request):
    """Страница со списком всех новостей"""
    news = Post.objects.filter(type='news').order_by('-created_at')
    news_count = news.count()

    # Для каждой новости обрезаем текст до 20 слов
    for item in news:
        words = item.text.split()
        item.short_text = ' '.join(words[:20]) + ('...' if len(words) > 20 else '')

    context = {
        'news': news,
        'news_count': news_count
    }
    return render(request, 'news_list.html', context)


def news_detail(request, news_id):
    """Детальная страница отдельной новости"""
    news_item = get_object_or_404(Post, id=news_id, type='news')

    context = {
        'news_item': news_item
    }
    return render(request, 'news_detail.html', context)