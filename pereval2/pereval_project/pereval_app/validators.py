"""
Валидаторы для моделей API
"""
import re
from django.core.exceptions import ValidationError


def validate_email(value: str) -> None:
    """Проверка корректности email"""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, value):
        raise ValidationError(f'{value} не является корректным email адресом')


def validate_phone(value: str) -> None:
    """Проверка корректности телефонного номера"""
    phone_regex = r'^\+?[0-9\s\-]{10,}$'
    if not re.match(phone_regex, value):
        raise ValidationError(f'{value} не является корректным телефонным номером')


def validate_coordinates(latitude: float, longitude: float) -> None:
    """Проверка корректности координат"""
    if latitude < -90 or latitude > 90:
        raise ValidationError('Широта должна быть в диапазоне от -90 до 90')
    if longitude < -180 or longitude > 180:
        raise ValidationError('Долгота должна быть в диапазоне от -180 до 180')


def validate_height(height: int) -> None:
    """Проверка высоты"""
    if height < 0:
        raise ValidationError('Высота не может быть отрицательной')
    if height > 8848:  # Эверест
        raise ValidationError('Слишком большая высота для горного перевала')


def validate_status(status: str) -> None:
    """Проверка статуса модерации"""
    valid_statuses = ['new', 'pending', 'accepted', 'rejected']
    if status not in valid_statuses:
        raise ValidationError(
            f'Недопустимый статус. Допустимые значения: {", ".join(valid_statuses)}'
        )