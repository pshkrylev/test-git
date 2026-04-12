from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Post, Category, CategorySubscriber
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_new_post_notification(post_id, category_id):
    """
    Асинхронная отправка уведомления подписчикам категории о новой статье
    """
    try:
        post = Post.objects.get(id=post_id)
        category = Category.objects.get(id=category_id)
        subscribers = category.subscribers.all()

        if not subscribers.exists():
            logger.info(f"Нет подписчиков для категории {category.name}")
            return

        post_url = f"{settings.SITE_URL}/news/{post.id}/"

        for subscriber in subscribers:
            try:
                # Отправляем письмо каждому подписчику
                send_mail(
                    subject=f'Новая статья в категории {category.name}',
                    message=render_to_string('email/new_post_notification.txt', {
                        'post': post,
                        'category': category,
                        'post_url': post_url,
                        'user': subscriber
                    }),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber.email],
                    fail_silently=False,
                    html_message=render_to_string('email/new_post_notification.html', {
                        'post': post,
                        'category': category,
                        'post_url': post_url,
                        'user': subscriber
                    })
                )
                logger.info(f"Уведомление отправлено пользователю {subscriber.email}")
            except Exception as e:
                logger.error(f"Ошибка при отправке пользователю {subscriber.email}: {e}")

        logger.info(f"Уведомления отправлены для статьи {post.title} в категории {category.name}")
    except Exception as e:
        logger.error(f"Ошибка в задаче send_new_post_notification: {e}")


@shared_task
def send_weekly_newsletter():
    """
    Асинхронная еженедельная рассылка новостей подписчикам
    """
    try:
        # Получаем дату неделю назад
        week_ago = timezone.now() - timedelta(days=7)

        # Получаем все категории
        categories = Category.objects.all()
        sent_count = 0

        for category in categories:
            # Получаем новые статьи за неделю в этой категории
            new_posts = category.posts.filter(
                created_at__gte=week_ago,
                type='news'
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
                    'created_at': post.created_at,
                    'preview': post.preview()
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
                    sent_count += 1
                    logger.info(f"Рассылка отправлена пользователю {subscriber.email} по категории {category.name}")
                except Exception as e:
                    logger.error(f"Ошибка при отправке рассылки пользователю {subscriber.email}: {e}")

        logger.info(f"Еженедельная рассылка завершена. Отправлено {sent_count} писем.")
    except Exception as e:
        logger.error(f"Ошибка в задаче send_weekly_newsletter: {e}")


@shared_task
def send_welcome_email(user_id):
    """
    Асинхронная отправка приветственного письма при регистрации
    """
    from django.contrib.auth.models import User
    from django.core.mail import send_mail
    from django.template.loader import render_to_string
    from django.conf import settings

    try:
        user = User.objects.get(id=user_id)

        send_mail(
            subject='Добро пожаловать на News Portal!',
            message=render_to_string('email/welcome_email.txt', {
                'user': user
            }),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
            html_message=render_to_string('email/welcome_email.html', {
                'user': user
            })
        )
        logger.info(f"Приветственное письмо отправлено пользователю {user.email}")
    except Exception as e:
        logger.error(f"Ошибка при отправке приветственного письма: {e}")