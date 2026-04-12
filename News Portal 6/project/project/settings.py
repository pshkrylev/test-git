import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-your-secret-key-here'

DEBUG = True  # Для разработки, при продакшене меняем на False

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'news',  # наше приложение
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'newsportal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'newsportal.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Создаем директорию для логов, если её нет
LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    # Форматтеры - определяем форматы вывода сообщений
    'formatters': {
        # Базовый формат для консоли (DEBUG и выше)
        'console_base': {
            'format': '{asctime} - {levelname} - {message}',
            'style': '{',
        },
        # Расширенный формат для консоли (WARNING и выше с pathname)
        'console_with_path': {
            'format': '{asctime} - {levelname} - {pathname} - {message}',
            'style': '{',
        },
        # Формат для general.log (INFO и выше)
        'general': {
            'format': '{asctime} - {levelname} - {module} - {message}',
            'style': '{',
        },
        # Формат для errors.log (ERROR и CRITICAL с exc_info)
        'error': {
            'format': '{asctime} - {levelname} - {pathname} - {message}\n{exc_info}',
            'style': '{',
        },
        # Формат для security.log
        'security': {
            'format': '{asctime} - {levelname} - {module} - {message}',
            'style': '{',
        },
        # Формат для отправки на почту
        'email': {
            'format': '{asctime} - {levelname} - {pathname} - {message}',
            'style': '{',
        },
    },

    # Фильтры
    'filters': {
        # Фильтр для консоли: сообщения отправляются только при DEBUG = True
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        # Фильтр для почты и general.log: сообщения отправляются только при DEBUG = False
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },

    # Обработчики - определяем, куда отправляем сообщения
    'handlers': {
        # Обработчик для консоли (уровень DEBUG и выше, базовый формат)
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],  # Только при DEBUG=True
            'formatter': 'console_base',
        },
        # Обработчик для консоли с pathname (уровень WARNING и выше)
        'console_warning': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],  # Только при DEBUG=True
            'formatter': 'console_with_path',
        },
        # Обработчик для файла general.log
        'general_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'general.log'),
            'filters': ['require_debug_false'],  # Только при DEBUG=False
            'formatter': 'general',
            'encoding': 'utf-8',
        },
        # Обработчик для файла errors.log
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'errors.log'),
            'formatter': 'error',
            'encoding': 'utf-8',
        },
        # Обработчик для файла security.log
        'security_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'security.log'),
            'formatter': 'security',
            'encoding': 'utf-8',
        },
        # Обработчик для отправки на почту
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],  # Только при DEBUG=False
            'formatter': 'email',
        },
    },

    # Логгеры - определяем источники сообщений
    'loggers': {
        # Основной логгер django (все сообщения)
        'django': {
            'handlers': ['console', 'console_warning', 'general_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        # Логгер django.request (HTTP запросы)
        'django.request': {
            'handlers': ['error_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        # Логгер django.server
        'django.server': {
            'handlers': ['error_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        # Логгер django.template
        'django.template': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        # Логгер django.db.backends
        'django.db.backends': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        # Логгер django.security
        'django.security': {
            'handlers': ['security_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Настройки для отправки почты (требуются при DEBUG=False)
"""
if not DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.yandex.ru'
    EMAIL_PORT = 465
    EMAIL_USE_SSL = True
    EMAIL_HOST_USER = 'your-email@example.com'
    EMAIL_HOST_PASSWORD = 'your-password'
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

    # Администраторы для получения логов
    ADMINS = [('Admin Name', 'admin@example.com')]
    SERVER_EMAIL = EMAIL_HOST_USER
"""