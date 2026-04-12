from functools import wraps
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from .models import Post


def cache_article(timeout=3600):
    """
    Декоратор для кэширования статей с автоматической инвалидацией
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            article_id = kwargs.get('pk')
            cache_key = f'article_view_{article_id}'

            # Пытаемся получить из кэша
            cached_response = cache.get(cache_key)
            if cached_response:
                return cached_response

            # Если нет в кэше, вызываем представление
            response = view_func(request, *args, **kwargs)

            # Сохраняем в кэш, только если статья существует
            if response.status_code == 200:
                cache.set(cache_key, response, timeout)

            return response

        return wrapper

    return decorator


def invalidate_article_cache_on_change(model_instance):
    """
    Функция для инвалидации кэша при изменении статьи
    """
    cache_key = f'article_view_{model_instance.id}'
    cache.delete(cache_key)

    # Также удаляем кэш для списков
    cache.delete_pattern('article_list*')
    cache.delete_pattern('category_articles_*')