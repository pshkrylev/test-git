"""
Мапперы для преобразования между JSON и моделями Django
"""

from .models import Pass, User, Coordinates, Level, Image


def pass_to_dict(pass_instance: Pass) -> dict:
    """
    Преобразование объекта Pass в словарь (JSON)
    """
    if not pass_instance:
        return {}

    return {
        'id': pass_instance.id,
        'beauty_title': pass_instance.beauty_title,
        'title': pass_instance.title,
        'other_titles': pass_instance.other_titles,
        'connect': pass_instance.connect,
        'add_time': pass_instance.add_time.isoformat(),
        'status': pass_instance.status,
        'status_display': pass_instance.get_status_display(),
        'moderation_comment': pass_instance.moderation_comment,
        'moderation_date': pass_instance.moderation_date.isoformat() if pass_instance.moderation_date else None,
        'user': {
            'email': pass_instance.user.email,
            'fam': pass_instance.user.fam,
            'name': pass_instance.user.name,
            'otc': pass_instance.user.otc,
            'phone': pass_instance.user.phone,
        },
        'coords': {
            'latitude': float(pass_instance.coords.latitude),
            'longitude': float(pass_instance.coords.longitude),
            'height': pass_instance.coords.height,
        },
        'level': {
            'winter': pass_instance.level.winter,
            'summer': pass_instance.level.summer,
            'autumn': pass_instance.level.autumn,
            'spring': pass_instance.level.spring,
        },
        'images': [
            {'data': img.data, 'title': img.title}
            for img in pass_instance.images.all()
        ]
    }


def user_from_dict(data: dict) -> User:
    """Создание объекта User из словаря (без сохранения)"""
    return User(
        email=data.get('email', ''),
        fam=data.get('fam', ''),
        name=data.get('name', ''),
        otc=data.get('otc', ''),
        phone=data.get('phone', '')
    )


def coordinates_from_dict(data: dict) -> Coordinates:
    """Создание объекта Coordinates из словаря (без сохранения)"""
    return Coordinates(
        latitude=data.get('latitude', 0),
        longitude=data.get('longitude', 0),
        height=data.get('height', 0)
    )


def level_from_dict(data: dict) -> Level:
    """Создание объекта Level из словаря (без сохранения)"""
    return Level(
        winter=data.get('winter', ''),
        summer=data.get('summer', ''),
        autumn=data.get('autumn', ''),
        spring=data.get('spring', '')
    )


def images_from_list(images_data: list) -> list:
    """Создание списка объектов Image из списка словарей"""
    images = []
    for img in images_data:
        images.append(Image(
            data=img.get('data', ''),
            title=img.get('title', '')
        ))
    return images


def pass_summary_to_dict(pass_instance: Pass) -> dict:
    """Краткое представление перевала для списка"""
    return {
        'id': pass_instance.id,
        'title': pass_instance.title,
        'beauty_title': pass_instance.beauty_title,
        'add_time': pass_instance.add_time.isoformat(),
        'status': pass_instance.status,
        'status_display': pass_instance.get_status_display(),
        'moderation_comment': pass_instance.moderation_comment,
        'user_email': pass_instance.user.email,
    }