from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Post, Category


@receiver([post_save, post_delete], sender=Post)
def invalidate_post_cache(sender, instance, **kwargs):
    """Очищает кэш при изменении или удалении новости"""
    # Очищаем кэш конкретной новости
    cache.delete(f'news_item_{instance.id}')

    # Очищаем кэш списка новостей
    cache.delete_pattern('news_list*')

    # Очищаем кэш популярных новостей
    cache.delete('sidebar_popular_posts')

    # Очищаем кэш главной страницы
    cache.delete('home_page')


@receiver([post_save, post_delete], sender=Category)
def invalidate_category_cache(sender, instance, **kwargs):
    """Очищает кэш категорий при их изменении"""
    cache.delete('sidebar_categories')