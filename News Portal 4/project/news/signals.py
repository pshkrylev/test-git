from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Post, Category, CategorySubscriber
import logging

logger = logging.getLogger(__name__)


@receiver(m2m_changed, sender=Post.categories.through)
def notify_subscribers_on_new_post(sender, instance, action, **kwargs):
    """
    Отправляет уведомление подписчикам категории при добавлении новой статьи
    """
    if action == 'post_add':
        post = instance
        categories = post.categories.all()

        for category in categories:
            subscribers = category.subscribers.all()

            for subscriber in subscribers:
                try:
                    # Формируем ссылку на статью
                    post_url = f"{settings.SITE_URL}/news/{post.id}/"

                    # Отправляем письмо
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
                    logger.info(f"Уведомление отправлено пользователю {subscriber.email} о статье {post.title}")
                except Exception as e:
                    logger.error(f"Ошибка при отправке уведомления пользователю {subscriber.email}: {e}")


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """Отправляет приветственное письмо при регистрации"""
    if created:
        try:
            send_mail(
                subject='Добро пожаловать на News Portal!',
                message=render_to_string('email/welcome_email.txt', {
                    'user': instance
                }),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                fail_silently=False,
                html_message=render_to_string('email/welcome_email.html', {
                    'user': instance
                })
            )
            logger.info(f"Приветственное письмо отправлено пользователю {instance.email}")
        except Exception as e:
            logger.error(f"Ошибка при отправке приветственного письма пользователю {instance.email}: {e}")