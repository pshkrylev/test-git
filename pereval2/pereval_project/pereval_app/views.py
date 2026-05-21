import json
import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .services import PerevalService

logger = logging.getLogger(__name__)


def cors_headers(response):
    """Добавление CORS заголовков к ответу"""
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, POST, PATCH, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


# ==================== POST /api/submitData/ ====================
@csrf_exempt
def submit_data(request):
    """Добавление нового перевала (Спринт 1)"""
    if request.method == 'OPTIONS':
        return cors_headers(JsonResponse({'status': 'ok'}))

    if request.method != 'POST':
        return cors_headers(JsonResponse(
            {'state': 0, 'message': 'Метод не разрешён', 'id': None},
            status=405
        ))

    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return cors_headers(JsonResponse(
            {'state': 0, 'message': 'Неверный формат JSON', 'id': None},
            status=400
        ))

    success, result, status_code = PerevalService.create_pass(data)
    return cors_headers(JsonResponse(result, status=status_code))


# ==================== GET /api/submitData/<id>/ ====================
@csrf_exempt
def get_pass(request, pk):
    """
     НОВЫЙ МЕТОД: получение одной записи по ID
    GET /api/submitData/<id>/
    """
    if request.method == 'OPTIONS':
        return cors_headers(JsonResponse({'status': 'ok'}))

    if request.method != 'GET':
        return cors_headers(JsonResponse(
            {'state': 0, 'message': 'Метод не разрешён'},
            status=405
        ))

    pass_instance = PerevalService.get_pass_by_id(pk)

    if not pass_instance:
        return cors_headers(JsonResponse(
            {'state': 0, 'message': f'Перевал с id {pk} не найден'},
            status=404
        ))

    data = {
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

    return cors_headers(JsonResponse(data, status=200))


# ==================== PATCH /api/submitData/<id>/ ====================
@csrf_exempt
def update_pass(request, pk):
    """
     НОВЫЙ МЕТОД: редактирование перевала
    PATCH /api/submitData/<id>/
    - Только если status = 'new'
    - Нельзя редактировать ФИО, email, телефон
    """
    if request.method == 'OPTIONS':
        return cors_headers(JsonResponse({'status': 'ok'}))

    if request.method != 'PATCH':
        return cors_headers(JsonResponse(
            {'state': 0, 'message': 'Метод не разрешён'},
            status=405
        ))

    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return cors_headers(JsonResponse(
            {'state': 0, 'message': 'Неверный формат JSON'},
            status=400
        ))

    success, result, http_status = PerevalService.update_pass(pk, data)
    return cors_headers(JsonResponse(result, status=http_status))


# ==================== GET /api/submitData/?user__email=<email> ====================
@csrf_exempt
def get_user_passes(request):
    """
     НОВЫЙ МЕТОД: список всех перевалов пользователя
    GET /api/submitData/?user__email=<email>
    """
    if request.method == 'OPTIONS':
        return cors_headers(JsonResponse({'status': 'ok'}))

    if request.method != 'GET':
        return cors_headers(JsonResponse(
            {'state': 0, 'message': 'Метод не разрешён'},
            status=405
        ))

    email = request.GET.get('user__email')
    if not email:
        return cors_headers(JsonResponse(
            {'state': 0, 'message': 'Параметр user__email обязателен'},
            status=400
        ))

    passes = PerevalService.get_passes_by_user(email)

    result = []
    for p in passes:
        result.append({
            'id': p.id,
            'title': p.title,
            'beauty_title': p.beauty_title,
            'add_time': p.add_time.isoformat(),
            'status': p.status,
            'status_display': p.get_status_display(),
            'moderation_comment': p.moderation_comment,
            'user_email': p.user.email,
        })

    return cors_headers(JsonResponse({
        'state': 1,
        'count': len(result),
        'results': result
    }, status=200))


# ==================== PATCH /api/submitData/<id>/status/ ====================
@csrf_exempt
def update_pass_status(request, pk):
    """Обновление статуса перевала (для сотрудников ФСТР)"""
    if request.method == 'OPTIONS':
        return cors_headers(JsonResponse({'status': 'ok'}))

    if request.method != 'PATCH':
        return cors_headers(JsonResponse(
            {'state': 0, 'message': 'Метод не разрешён'},
            status=405
        ))

    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return cors_headers(JsonResponse(
            {'state': 0, 'message': 'Неверный формат JSON'},
            status=400
        ))

    new_status = data.get('status')
    if not new_status:
        return cors_headers(JsonResponse(
            {'state': 0, 'message': 'Поле "status" обязательно'},
            status=400
        ))

    comment = data.get('comment', '')
    moderator_id = data.get('moderator_id')

    success, result, http_status = PerevalService.update_status(
        pass_id=pk,
        new_status=new_status,
        moderator_id=moderator_id,
        comment=comment
    )

    return cors_headers(JsonResponse(result, status=http_status))


# ==================== GET /api/submitData/status/<status>/ ====================
@csrf_exempt
def get_passes_by_status(request, status):
    """Получение перевалов по статусу (для модераторов)"""
    if request.method == 'OPTIONS':
        return cors_headers(JsonResponse({'status': 'ok'}))

    if request.method != 'GET':
        return cors_headers(JsonResponse(
            {'state': 0, 'message': 'Метод не разрешён'},
            status=405
        ))

    passes = PerevalService.get_passes_by_status(status)

    result = []
    for p in passes:
        result.append({
            'id': p.id,
            'title': p.title,
            'add_time': p.add_time.isoformat(),
            'user_email': p.user.email,
            'moderation_comment': p.moderation_comment,
        })

    return cors_headers(JsonResponse({
        'status': status,
        'count': len(result),
        'results': result
    }, status=200))