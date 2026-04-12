from django.db import models
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Post(models.Model):
    # ... существующие поля ...

    def save(self, *args, **kwargs):
        """Переопределяем save для очистки кэша"""
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Очищаем кэш при сохранении
        if not is_new:
            self.clear_cache()

    def delete(self, *args, **kwargs):
        """Очищаем кэш при удалении"""
        self.clear_cache()
        super().delete(*args, **kwargs)

    def clear_cache(self):
        """Очищает кэш для этой статьи"""
        cache_key = f'article_{self.id}'
        cache.delete(cache_key)

        # Очищаем кэш списков
        cache.delete_pattern('article_list*')
        cache.delete_pattern(f'category_articles_*')
        cache.delete('popular_articles')

    @classmethod
    def get_cached_article(cls, article_id):
        """Статический метод для получения кэшированной статьи"""
        from .utils import get_cached_article
        return get_cached_article(article_id)


@receiver(post_save, sender=Post)
def clear_article_cache_on_save(sender, instance, **kwargs):
    """Сигнал для очистки кэша при сохранении"""
    if instance.type == 'article':
        instance.clear_cache()


@receiver(post_delete, sender=Post)
def clear_article_cache_on_delete(sender, instance, **kwargs):
    """Сигнал для очистки кэша при удалении"""
    if instance.type == 'article':
        cache_key = f'article_{instance.id}'
        cache.delete(cache_key)