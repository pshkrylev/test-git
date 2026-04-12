import logging
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

# Получаем логгеры
logger = logging.getLogger('django')
request_logger = logging.getLogger('django.request')
security_logger = logging.getLogger('django.security')


def test_logging(request):
    """Тестовая функция для проверки всех уровней логирования"""

    # 1. Проверка основного логгера django
    logger.debug("DEBUG сообщение - только в консоль (при DEBUG=True)")
    logger.info("INFO сообщение - в консоль и general.log (при DEBUG=False)")
    logger.warning("WARNING сообщение - в консоль с pathname")

    # 2. Проверка ошибок с exc_info
    try:
        # Имитация ошибки
        result = 10 / 0
    except ZeroDivisionError as e:
        logger.error("ERROR: Деление на ноль", exc_info=True)
        logger.critical("CRITICAL: Серьезная ошибка", exc_info=True)

    # 3. Проверка логгера django.request
    try:
        # Имитация ошибки запроса
        raise PermissionDenied("Доступ запрещен")
    except PermissionDenied as e:
        request_logger.error("Ошибка доступа к ресурсу", exc_info=True)

    # 4. Проверка логгера django.security
    security_logger.warning("Подозрительная активность: множественные попытки входа")
    security_logger.error("Нарушение безопасности: SQL инъекция обнаружена")

    return HttpResponse("Логирование проверено! Смотрите консоль и файлы в папке logs/")