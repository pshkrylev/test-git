from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.responses.models import Response
from .tasks import send_response_notification

@receiver(post_save, sender=Response)
def notify_post_owner(sender, instance, created, **kwargs):
    if created:
        send_response_notification.delay(instance.id)