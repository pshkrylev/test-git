from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_response_notification(response_id):
    from apps.responses.models import Response
    response = Response.objects.select_related('post__author', 'author').get(id=response_id)
    send_mail(
        subject=f'Новый отклик на "{response.post.title}"',
        message=f'''Здравствуйте, {response.post.author.username}!

Пользователь {response.author.username} оставил отклик на ваше объявление "{response.post.title}".

Текст отклика:
{response.text}

Перейдите в личный кабинет для принятия или отклонения отклика.

С уважением,
Команда MMORPG Board''',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[response.post.author.email],
        fail_silently=False,
    )

@shared_task
def send_acceptance_notification(response_id):
    from apps.responses.models import Response
    response = Response.objects.select_related('post', 'author').get(id=response_id)
    send_mail(
        subject=f'Ваш отклик на "{response.post.title}" принят!',
        message=f'''Здравствуйте, {response.author.username}!

Автор объявления "{response.post.title}" принял ваш отклик.

Свяжитесь с автором для дальнейшего обсуждения.

С уважением,
Команда MMORPG Board''',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[response.author.email],
        fail_silently=False,
    )