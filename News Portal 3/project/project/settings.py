import os

# Добавляем allauth в INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # требуется для allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',  # провайдер Yandex
    'news',  # ваше приложение
]

# Настройки сайта для allauth
SITE_ID = 1

# Перенаправления
LOGIN_URL = '/accounts/login/'  # адрес для перенаправления на страницу входа
LOGIN_REDIRECT_URL = '/news/'   # адрес перенаправления после успешного входа
LOGOUT_REDIRECT_URL = '/news/'  # адрес перенаправления после выхода

# Настройки allauth
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # для упрощения, можно 'mandatory'

# Настройки email (для тестирования)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Настройки Yandex (для продакшена)
SOCIALACCOUNT_PROVIDERS = {
    'yandex': {
        'APP': {
            'client_id': 'YOUR_CLIENT_ID',
            'secret': 'YOUR_SECRET_KEY',
            'key': ''
        }
    }
}

# Аутентификация через allauth
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]