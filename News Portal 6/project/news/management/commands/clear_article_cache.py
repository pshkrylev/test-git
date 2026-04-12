from django.core.management.base import BaseCommand
from django.core.cache import cache
from news.models import Post


class Command(BaseCommand):
    help = 'Очищает кэш статей'

    def add_arguments(self, parser):
        parser.add_argument(
            '--article-id',
            type=int,
            help='ID конкретной статьи для очистки кэша'
        )

    def handle(self, *args, **options):
        article_id = options.get('article_id')

        if article_id:
            # Очищаем кэш конкретной статьи
            cache_key = f'article_{article_id}'
            cache.delete(cache_key)
            cache.delete(f'article_view_{article_id}')
            self.stdout.write(self.style.SUCCESS(f'Кэш статьи {article_id} очищен'))
        else:
            # Очищаем кэш всех статей
            articles = Post.objects.filter(type='article')
            count = 0

            for article in articles:
                cache_key = f'article_{article.id}'
                if cache.delete(cache_key):
                    count += 1
                cache.delete(f'article_view_{article.id}')

            # Очищаем кэш списков
            cache.delete_pattern('article_list*')
            cache.delete_pattern('category_articles_*')
            cache.delete('popular_articles')

            self.stdout.write(self.style.SUCCESS(f'Очищен кэш для {count} статей'))