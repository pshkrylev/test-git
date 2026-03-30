from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from news.models import Category, Post
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Отправляет еженедельную рассылку новостей подписчикам категорий'

    def handle(self, *args, **options):
        self.stdout.write('Начинаем отправку еженедельной рассылки...')

        # Получаем дату неделю назад
        week_ago = timezone.now() - timedelta(days=7)

        # Получаем все категории
        categories = Category.objects.all()

        for category in categories:
            # Получаем новые статьи за неделю в этой категории
            new_posts = category.posts.filter(
                created_at__gte=week_ago,
                type='news'  # или 'article' в зависимости от вашей логики
            ).order_by('-created_at')

            if not new_posts.exists():
                continue

            # Получаем подписчиков категории
            subscribers = category.subscribers.all()

            if not subscribers.exists():
                continue

            # Формируем список статей с ссылками
            posts_with_urls = []
            for post in new_posts:
                posts_with_urls.append({
                    'title': post.title,
                    'url': f"{settings.SITE_URL}/news/{post.id}/",
                    'created_at': post.created_at
                })

            # Отправляем письмо каждому подписчику
            for subscriber in subscribers:
                try:
                    send_mail(
                        subject=f'Еженедельная рассылка: новые статьи в категории {category.name}',
                        message=render_to_string('email/weekly_newsletter.txt', {
                            'user': subscriber,
                            'category': category,
                            'posts': posts_with_urls,
                            'week_ago': week_ago
                        }),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[subscriber.email],
                        fail_silently=False,
                        html_message=render_to_string('email/weekly_newsletter.html', {
                            'user': subscriber,
                            'category': category,
                            'posts': posts_with_urls,
                            'week_ago': week_ago
                        })
                    )
                    logger.info(
                        f"Еженедельная рассылка отправлена пользователю {subscriber.email} по категории {category.name}")
                except Exception as e:
                    logger.error(f"Ошибка при отправке рассылки пользователю {subscriber.email}: {e}")

        self.stdout.write(self.style.SUCCESS('Еженедельная рассылка завершена'))