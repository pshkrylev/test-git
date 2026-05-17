import json
import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .services import PerevalService

logger = logging.getLogger(__name__)


@csrf_exempt
def submit_data(request):
    """POST /api/submitData/ - добавление перевала"""
    if request.method == 'OPTIONS':
        response = JsonResponse({'status': 'ok'})
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    if request.method != 'POST':
        return JsonResponse(
            {'status': 405, 'message': 'Метод не разрешён', 'id': None},
            status=405
        )

    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse(
            {'status': 400, 'message': 'Неверный формат JSON', 'id': None},
            status=400
        )

    success, result, status_code = PerevalService.create_pass(data)

    response = JsonResponse(result, status=status_code)
    response['Access-Control-Allow-Origin'] = '*'
    return response


@csrf_exempt
def get_pass(request, pk):
    """GET /api/submitData/<id>/ - получение перевала"""
    if request.method == 'OPTIONS':
        response = JsonResponse({'status': 'ok'})
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        return response

    if request.method != 'GET':
        return JsonResponse(
            {'status': 405, 'message': 'Метод не разрешён'},
            status=405
        )

    pass_instance = PerevalService.get_pass_by_id(pk)

    if not pass_instance:
        return JsonResponse(
            {'status': 404, 'message': f'Перевал с id {pk} не найден'},
            status=404
        )

    data = {
        'id': pass_instance.id,
        'beauty_title': pass_instance.beauty_title,
        'title': pass_instance.title,
        'other_titles': pass_instance.other_titles,
        'connect': pass_instance.connect,
        'add_time': pass_instance.add_time.isoformat(),
        'status': pass_instance.status,
        'status_display': pass_instance.get_status_display(),
        'moderation_comment': pass_instance.moderation_comment,  # ⭐ НОВОЕ ПОЛЕ
        'moderation_date': pass_instance.moderation_date.isoformat() if pass_instance.moderation_date else None,
        # ⭐ НОВОЕ ПОЛЕ
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
        'images': [
            {'data': img.data, 'title': img.title}
            for img in pass_instance.images.all()
        ]
    }

    response = JsonResponse(data, status=200)
    response['Access-Control-Allow-Origin'] = '*'
    return response


@csrf_exempt
def update_pass(request, pk):
    """PATCH /api/submitData/<id>/edit/ - редактирование перевала"""
    if request.method == 'OPTIONS':
        response = JsonResponse({'status': 'ok'})
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'PATCH, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    if request.method != 'PATCH':
        return JsonResponse(
            {'state': 0, 'message': 'Метод не разрешён'},
            status=405
        )

    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse(
            {'state': 0, 'message': 'Неверный формат JSON'},
            status=400
        )

    success, result, http_status = PerevalService.update_pass(pk, data)

    response = JsonResponse(result, status=http_status)
    response['Access-Control-Allow-Origin'] = '*'
    return response


@csrf_exempt
def update_pass_status(request, pk):
    """
    ⭐ ОБНОВЛЁННЫЙ МЕТОД: PATCH /api/submitData/<id>/status/
    Обновление статуса перевала с комментарием модератора

    Пример запроса:
    {
        "status": "rejected",
        "comment": "Не указана высота перевала"
    }

    или

    {
        "status": "accepted",
        "comment": "Отличный перевал, информация подтверждена"
    }
    """
    if request.method == 'OPTIONS':
        response = JsonResponse({'status': 'ok'})
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'PATCH, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    if request.method != 'PATCH':
        return JsonResponse(
            {'state': 0, 'message': 'Метод не разрешён'},
            status=405
        )

    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse(
            {'state': 0, 'message': 'Неверный формат JSON'},
            status=400
        )

    new_status = data.get('status')
    if not new_status:
        return JsonResponse(
            {'state': 0, 'message': 'Поле "status" обязательно'},
            status=400
        )

    # Получаем комментарий из запроса
    comment = data.get('comment', '')

    # Можно передавать ID модератора (например, из токена авторизации)
    moderator_id = data.get('moderator_id')

    success, result, http_status = PerevalService.update_status(
        pass_id=pk,
        new_status=new_status,
        moderator_id=moderator_id,
        comment=comment
    )

    response = JsonResponse(result, status=http_status)
    response['Access-Control-Allow-Origin'] = '*'
    return response


@csrf_exempt
def get_passes_by_user(request):
    """GET /api/submitData/?user__email=<email> - фильтрация по email"""
    if request.method == 'OPTIONS':
        response = JsonResponse({'status': 'ok'})
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        return response

    if request.method != 'GET':
        return JsonResponse(
            {'status': 405, 'message': 'Метод не разрешён'},
            status=405
        )

    email = request.GET.get('user__email')
    if not email:
        return JsonResponse(
            {'status': 400, 'message': 'Параметр user__email обязателен'},
            status=400
        )

    passes = PerevalService.get_passes_by_user_email(email)

    result = []
    for p in passes:
        result.append({
            'id': p.id,
            'title': p.title,
            'status': p.status,
            'status_display': p.get_status_display(),
            'moderation_comment': p.moderation_comment,  # ⭐ НОВОЕ ПОЛЕ
            'add_time': p.add_time.isoformat(),
            'user_email': p.user.email,
        })

    response = JsonResponse({'results': result, 'count': len(result)}, status=200)
    response['Access-Control-Allow-Origin'] = '*'
    return response