from django.contrib import admin
from django.core.mail import send_mass_mail
from django.conf import settings
from .models import Newsletter
from apps.accounts.models import User


@admin.action(description='Отправить выбранные рассылки')
def send_newsletter(modeladmin, request, queryset):
    for nl in queryset:
        if nl.is_sent:
            modeladmin.message_user(request, f'Рассылка "{nl.subject}" уже отправлена', level='ERROR')
            continue
        users = User.objects.filter(subscribed_to_news=True, is_verified=True)
        emails = list(users.values_list('email', flat=True))
        if not emails:
            modeladmin.message_user(request, 'Нет подписанных пользователей', level='WARNING')
            continue
        messages = [(nl.subject, nl.message, settings.DEFAULT_FROM_EMAIL, [email]) for email in emails]
        send_mass_mail(messages, fail_silently=False)
        nl.is_sent = True
        nl.save()
        modeladmin.message_user(request, f'Рассылка "{nl.subject}" отправлена {len(emails)} пользователям')


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject', 'is_sent', 'sent_at')
    list_filter = ('is_sent', 'sent_at')
    search_fields = ('subject',)
    readonly_fields = ('sent_at',)
    actions = [send_newsletter]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.is_sent = False
        super().save_model(request, obj, form, change)