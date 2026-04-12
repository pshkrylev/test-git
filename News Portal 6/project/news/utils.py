from django.core.cache import cache
from .models import Post


def get_cached_article(article_id):
    """
    Получает статью из кэша или из базы данных
    """
    cache_key = f'article_{article_id}'
    article = cache.get(cache_key)

    if not article:
        try:
            article = Post.objects.get(id=article_id, type='article')
            # Кэшируем статью на 1 час (или пока не изменится)
            cache.set(cache_key, article, timeout=3600)
        except Post.DoesNotExist:
            return None

    return article


def invalidate_article_cache(article):
    """
    Очищает кэш для конкретной статьи
    """
    cache_key = f'article_{article.id}'
    cache.delete(cache_key)

    # Также очищаем связанные кэши
    cache.delete_pattern('article_list*')
    cache.delete_pattern('category_articles_*')
    cache.delete('popular_articles')


def get_cached_article_list(category_id=None, limit=10):
    """
    Получает список статей из кэша
    """
    cache_key = f'article_list_{category_id}_{limit}'
    articles = cache.get(cache_key)

    if not articles:
        queryset = Post.objects.filter(type='article')
        if category_id:
            queryset = queryset.filter(categories__id=category_id)
        articles = list(queryset.order_by('-created_at')[:limit])
        cache.set(cache_key, articles, timeout=1800)  # Кэш на 30 минут

    return articles


def get_cached_article_rating(article_id):
    """
    Получает рейтинг статьи из кэша
    """
    cache_key = f'article_rating_{article_id}'
    rating = cache.get(cache_key)

    if rating is None:
        article = Post.objects.get(id=article_id, type='article')
        rating = article.rating
        cache.set(cache_key, rating, timeout=300)  # Кэш на 5 минут

    return rating


def update_article_rating_cache(article_id, new_rating):
    """
    Обновляет кэш рейтинга статьи
    """
    cache_key = f'article_rating_{article_id}'
    cache.set(cache_key, new_rating, timeout=300)