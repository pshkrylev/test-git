from django.core.cache import cache
from .models import Category, Post


def categories_processor(request):
    """Контекстный процессор для категорий и популярных новостей с кэшированием"""

    # Кэшируем категории на 30 минут
    categories = cache.get('sidebar_categories')
    if not categories:
        categories = Category.objects.all()
        cache.set('sidebar_categories', categories, 1800)  # 30 минут

    # Кэшируем популярные новости на 15 минут
    popular_posts = cache.get('sidebar_popular_posts')
    if not popular_posts:
        popular_posts = Post.objects.filter(type='news').order_by('-rating')[:5]
        cache.set('sidebar_popular_posts', popular_posts, 900)  # 15 минут

    return {
        'categories': categories,
        'popular_posts': popular_posts
    }