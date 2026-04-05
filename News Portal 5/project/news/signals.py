from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import Post, Category
from .tasks import send_new_post_notification, send_welcome_email
import logging

logger = logging.getLogger(__name__)


@receiver(m2m_changed, sender=Post.categories.through)
def notify_subscribers_on_new_post(sender, instance, action, **kwargs):
    """
    Отправляет асинхронное уведомление подписчикам категории при добавлении новой статьи
    """
    if action == 'post_add':
        post = instance
        categories = post.categories.all()

        for category in categories:
            # Запускаем асинхронную задачу
            send_new_post_notification.delay(post.id, category.id)
            logger.info(f"Запущена асинхронная задача для статьи {post.title} и категории {category.name}")


@receiver(post_save, sender=User)
def add_user_to_common_group(sender, instance, created, **kwargs):
    """Автоматически добавляет новых пользователей в группу common и отправляет приветствие"""
    if created:
        common_group, _ = Group.objects.get_or_create(name='common')
        instance.groups.add(common_group)

        # Запускаем асинхронную отправку приветственного письма
        from .tasks import send_welcome_email
        send_welcome_email.delay(instance.id)
        logger.info(f"Запущена асинхронная задача приветственного письма для {instance.email}")