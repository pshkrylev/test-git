"""Мапперы для преобразования между JSON и моделями"""


def map_pass_to_json(pass_instance):
    """Преобразование объекта Pass в JSON"""
    if not pass_instance:
        return None

    return {
        'id': pass_instance.id,
        'beauty_title': pass_instance.beauty_title,
        'title': pass_instance.title,
        'other_titles': pass_instance.other_titles,
        'connect': pass_instance.connect,
        'add_time': pass_instance.add_time.isoformat(),
        'status': pass_instance.status,
        'user': {
            'email': pass_instance.user.email,
            'fam': pass_instance.user.fam,
            'name': pass_instance.user.name,
            'otc': pass_instance.user.otc,
            'phone': pass_instance.user.phone,
        },
        'coords': {
            'latitude': pass_instance.coords.latitude,
            'longitude': pass_instance.coords.longitude,
            'height': pass_instance.coords.height,
        },
        'level': {
            'winter': pass_instance.level.winter,
            'summer': pass_instance.level.summer,
            'autumn': pass_instance.level.autumn,
            'spring': pass_instance.level.spring,
        },
        'images': [{'data': img.data, 'title': img.title} for img in pass_instance.images.all()]
    }


def map_json_to_pass(data):
    """Преобразование JSON в объект Pass (без сохранения)"""
    from .models import User, Coordinates, Level, Image

    user_data = data.get('user', {})
    coords_data = data.get('coords', {})
    level_data = data.get('level', {})
    images_data = data.get('images', [])

    return {
        'beauty_title': data.get('beauty_title', ''),
        'title': data.get('title', ''),
        'other_titles': data.get('other_titles', ''),
        'connect': data.get('connect', ''),
        'user': User(
            email=user_data.get('email'),
            fam=user_data.get('fam', ''),
            name=user_data.get('name', ''),
            otc=user_data.get('otc', ''),
            phone=user_data.get('phone', '')
        ),
        'coords': Coordinates(
            latitude=coords_data.get('latitude'),
            longitude=coords_data.get('longitude'),
            height=coords_data.get('height')
        ),
        'level': Level(
            winter=level_data.get('winter', ''),
            summer=level_data.get('summer', ''),
            autumn=level_data.get('autumn', ''),
            spring=level_data.get('spring', '')
        ),
        'images': [
            Image(data=img.get('data'), title=img.get('title', ''))
            for img in images_data
        ]
    }