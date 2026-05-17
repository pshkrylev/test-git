from django.core.exceptions import ValidationError
import re


def validate_email(value):
    """Проверка корректности email"""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, value):
        raise ValidationError(f'{value} не является корректным email адресом')


def validate_phone(value):
    """Проверка корректности телефонного номера"""
    phone_regex = r'^\+?[0-9\s\-]{10,}$'
    if not re.match(phone_regex, value):
        raise ValidationError(f'{value} не является корректным телефонным номером')


def validate_coordinates(lat, lon):
    """Проверка корректности координат"""
    if lat < -90 or lat > 90:
        raise ValidationError('Широта должна быть в диапазоне от -90 до 90')
    if lon < -180 or lon > 180:
        raise ValidationError('Долгота должна быть в диапазоне от -180 до 180')


def validate_height(value):
    """Проверка высоты"""
    if value < 0:
        raise ValidationError('Высота не может быть отрицательной')
    if value > 8848:  # Эверест
        raise ValidationError('Слишком большая высота для горного перевала')