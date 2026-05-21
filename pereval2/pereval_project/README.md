# Pereval API — REST API для ФСТР (горные перевалы)

##  Описание проекта

API для мобильного приложения туристов. Позволяет:
- Добавлять информацию о горных перевалах
- Редактировать данные (только в статусе `new`)
- Просматривать статус модерации
- Получать список всех перевалов пользователя

##  Технологии

- Python 3.11
- Django 4.2
- Django REST Framework
- PostgreSQL
- Swagger (drf-yasg)
- Gunicorn

##  Быстрый старт

### Локальный запуск

```bash
# Клонирование репозитория
git clone https://github.com/your-username/pereval-api.git
cd pereval-api

# Виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Установка зависимостей
pip install -r requirements.txt

# Переменные окружения (создать .env)
cp .env.example .env
# Заполнить FSTR_DB_HOST, FSTR_DB_PORT, FSTR_DB_LOGIN, FSTR_DB_PASS

# Миграции
python manage.py migrate

# Запуск сервера
python manage.py runserver