import os

# Настройки email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'  # или другой SMTP-сервер
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'your_email@yandex.ru'
EMAIL_HOST_PASSWORD = 'your_password'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SITE_URL = 'http://127.0.0.1:8000'  # URL вашего сайта

# Настройки планировщика
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25