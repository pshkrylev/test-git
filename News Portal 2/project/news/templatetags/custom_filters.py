from django import template
from django.template.defaultfilters import stringfilter
from django.template import TemplateSyntaxError
import re

register = template.Library()

# Список нецензурных слов для цензурирования
BAD_WORDS = [
    'редиска', 'дурак', 'болван', 'негодяй', 'идиот',
    'кретин', 'дебил', 'придурок', 'тупица'
]


@register.filter(name='censor')
@stringfilter
def censor(value):
    """
    Фильтр для цензурирования нецензурных слов.
    Заменяет все буквы слова, кроме первой, на звездочки.

    Args:
        value (str): Строка для цензурирования

    Returns:
        str: Строка с замененными нецензурными словами

    Raises:
        TemplateSyntaxError: Если фильтр применен не к строке
    """
    if not isinstance(value, str):
        raise TemplateSyntaxError(
            "Фильтр 'censor' может применяться только к строковым значениям. "
            f"Получен тип: {type(value).__name__}"
        )

    result = value

    for bad_word in BAD_WORDS:
        # Создаем паттерн для поиска слова
        # \b - граница слова, [верхний|нижний] регистр первой буквы, остальные буквы в нижнем
        pattern = r'\b[' + bad_word[0].upper() + bad_word[0].lower() + r']' + bad_word[1:] + r'\b'

        def replace_func(match):
            word = match.group(0)
            # Сохраняем первую букву, остальные заменяем звездочками
            return word[0] + '*' * (len(word) - 1)

        result = re.sub(pattern, replace_func, result, flags=re.IGNORECASE)

    return result