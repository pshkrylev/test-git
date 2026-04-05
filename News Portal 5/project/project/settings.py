import os

# Настройки Celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Redis как брокер
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # Хранение результатов
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_BEAT_SCHEDULE = {
    'send_weekly_newsletter': {
        'task': 'news.tasks.send_weekly_newsletter',
        'schedule': crontab(day_of_week='monday', hour=8, minute=0),  # каждый понедельник в 8:00
    },
}

# Настройки email (для отправки писем)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'  # или другой SMTP-сервер
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'your_email@yandex.ru'
EMAIL_HOST_PASSWORD = 'your_password'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SITE_URL = 'http://127.0.0.1:8000'  # URL вашего сайта