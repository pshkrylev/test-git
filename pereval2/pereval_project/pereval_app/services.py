import logging
from django.db import transaction
from django.utils import timezone
from .models import User, Coordinates, Level, Image, Pass

logger = logging.getLogger(__name__)


class PerevalService:
    """Класс для работы с базой данных (CRUD для перевалов)"""

    # ==================== ПОЛЬЗОВАТЕЛИ ====================

    @staticmethod
    def get_or_create_user(user_data: dict) -> User:
        """Получить или создать пользователя по email"""
        email = user_data.get('email')
        if not email:
            raise ValueError("Email пользователя обязателен")

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'fam': user_data.get('fam', ''),
                'name': user_data.get('name', ''),
                'otc': user_data.get('otc', ''),
                'phone': user_data.get('phone', ''),
            }
        )

        if not created:
            user.fam = user_data.get('fam', user.fam)
            user.name = user_data.get('name', user.name)
            user.otc = user_data.get('otc', user.otc)
            user.phone = user_data.get('phone', user.phone)
            user.save()

        return user

    # ==================== ВАЛИДАЦИЯ ====================

    @staticmethod
    def validate_data(data: dict) -> tuple[bool, str]:
        """Валидация входных данных при создании"""
        required_fields = ['user', 'coords', 'level', 'title']
        for field in required_fields:
            if field not in data:
                return False, f"Отсутствует поле: {field}"

        user_data = data.get('user', {})
        required_user_fields = ['email', 'fam', 'name', 'phone']
        for field in required_user_fields:
            if not user_data.get(field):
                return False, f"Отсутствует поле пользователя: {field}"

        coords = data.get('coords', {})
        required_coords = ['latitude', 'longitude', 'height']
        for field in required_coords:
            if field not in coords:
                return False, f"Отсутствует поле координат: {field}"

        return True, "OK"

    @staticmethod
    def validate_update_data(data: dict, existing_pass: Pass) -> tuple[bool, str]:
        """
        Валидация данных при редактировании.
        Запрещаем редактировать: ФИО, email, телефон.
        """
        forbidden_fields = []

        if 'user' in data:
            user_data = data['user']
            if 'fam' in user_data and user_data['fam'] != existing_pass.user.fam:
                forbidden_fields.append('Фамилия')
            if 'name' in user_data and user_data['name'] != existing_pass.user.name:
                forbidden_fields.append('Имя')
            if 'otc' in user_data and user_data['otc'] != existing_pass.user.otc:
                forbidden_fields.append('Отчество')
            if 'email' in user_data and user_data['email'] != existing_pass.user.email:
                forbidden_fields.append('Email')
            if 'phone' in user_data and user_data['phone'] != existing_pass.user.phone:
                forbidden_fields.append('Телефон')

        if forbidden_fields:
            return False, f"Редактирование следующих полей запрещено: {', '.join(forbidden_fields)}"

        return True, "OK"

    # ==================== CRUD ДЛЯ ПЕРЕВАЛОВ ====================

    @staticmethod
    @transaction.atomic
    def create_pass(data: dict) -> tuple[bool, dict, int]:
        """Создание нового перевала (статус 'new')"""
        try:
            is_valid, msg = PerevalService.validate_data(data)
            if not is_valid:
                return False, {'state': 0, 'message': msg, 'id': None}, 400

            user = PerevalService.get_or_create_user(data['user'])

            coords_data = data['coords']
            coords = Coordinates.objects.create(
                latitude=coords_data['latitude'],
                longitude=coords_data['longitude'],
                height=coords_data['height']
            )

            level_data = data['level']
            level = Level.objects.create(
                winter=level_data.get('winter', ''),
                summer=level_data.get('summer', ''),
                autumn=level_data.get('autumn', ''),
                spring=level_data.get('spring', '')
            )

            pass_instance = Pass.objects.create(
                beauty_title=data.get('beauty_title', ''),
                title=data['title'],
                other_titles=data.get('other_titles', ''),
                connect=data.get('connect', ''),
                user=user,
                coords=coords,
                level=level
            )

            images_data = data.get('images', [])
            for img in images_data:
                image = Image.objects.create(
                    data=img.get('data'),
                    title=img.get('title', '')
                )
                pass_instance.images.add(image)

            logger.info(f"Перевал создан: id={pass_instance.id}, title={pass_instance.title}")

            return True, {
                'state': 1,
                'message': 'Отправлено успешно',
                'id': pass_instance.id
            }, 200

        except Exception as e:
            logger.error(f"Ошибка при создании перевала: {str(e)}")
            return False, {
                'state': 0,
                'message': f'Ошибка сервера: {str(e)}',
                'id': None
            }, 500

    #  НОВЫЙ МЕТОД: получение перевала по ID
    @staticmethod
    def get_pass_by_id(pass_id: int) -> Pass | None:
        """Получение перевала по ID со всеми связанными данными"""
        try:
            return Pass.objects.select_related(
                'user', 'coords', 'level', 'moderated_by'
            ).prefetch_related('images').get(id=pass_id)
        except Pass.DoesNotExist:
            return None

    #  НОВЫЙ МЕТОД: редактирование перевала (с проверками)
    @staticmethod
    def update_pass(pass_id: int, data: dict) -> tuple[bool, dict, int]:
        """
        Редактирование перевала
        - Только если status == 'new'
        - Нельзя редактировать ФИО, email, телефон
        """
        try:
            pass_instance = Pass.objects.get(id=pass_id)

            # Проверка статуса
            if pass_instance.status != Pass.Status.NEW:
                return False, {
                    'state': 0,
                    'message': f'Нельзя редактировать перевал в статусе "{pass_instance.get_status_display()}". '
                               f'Доступно только для статуса "new"'
                }, 400

            # Валидация запрещённых полей
            is_valid, msg = PerevalService.validate_update_data(data, pass_instance)
            if not is_valid:
                return False, {'state': 0, 'message': msg}, 400

            # Обновление основных полей перевала
            if 'title' in data:
                pass_instance.title = data['title']
            if 'beauty_title' in data:
                pass_instance.beauty_title = data['beauty_title']
            if 'other_titles' in data:
                pass_instance.other_titles = data['other_titles']
            if 'connect' in data:
                pass_instance.connect = data['connect']

            # Обновление координат
            if 'coords' in data:
                coords = pass_instance.coords
                if 'latitude' in data['coords']:
                    coords.latitude = float(data['coords']['latitude'])
                if 'longitude' in data['coords']:
                    coords.longitude = float(data['coords']['longitude'])
                if 'height' in data['coords']:
                    coords.height = int(data['coords']['height'])
                coords.save()

            # Обновление уровня сложности
            if 'level' in data:
                level = pass_instance.level
                if 'winter' in data['level']:
                    level.winter = data['level']['winter']
                if 'summer' in data['level']:
                    level.summer = data['level']['summer']
                if 'autumn' in data['level']:
                    level.autumn = data['level']['autumn']
                if 'spring' in data['level']:
                    level.spring = data['level']['spring']
                level.save()

            # Добавление новых изображений (старые не удаляем по ТЗ)
            if 'images' in data and data['images']:
                for img_data in data['images']:
                    image = Image.objects.create(
                        data=img_data.get('data'),
                        title=img_data.get('title', '')
                    )
                    pass_instance.images.add(image)

            pass_instance.save()

            logger.info(f"Перевал {pass_id} успешно обновлён пользователем {pass_instance.user.email}")

            return True, {
                'state': 1,
                'message': 'Запись успешно обновлена'
            }, 200

        except Pass.DoesNotExist:
            return False, {'state': 0, 'message': f'Перевал с id {pass_id} не найден'}, 404
        except Exception as e:
            logger.error(f"Ошибка при обновлении перевала: {str(e)}")
            return False, {'state': 0, 'message': f'Ошибка: {str(e)}'}, 500

    #  НОВЫЙ МЕТОД: получение всех перевалов пользователя по email
    @staticmethod
    def get_passes_by_user(email: str):
        """Получение всех перевалов пользователя с их статусами"""
        if not email:
            return Pass.objects.none()

        return Pass.objects.filter(user__email=email).select_related(
            'user', 'coords', 'level'
        ).prefetch_related('images').order_by('-add_time')

    @staticmethod
    def get_passes_by_status(status: str):
        """Получение перевалов по статусу (для модераторов)"""
        valid_statuses = ['new', 'pending', 'accepted', 'rejected']
        if status not in valid_statuses:
            return Pass.objects.none()

        return Pass.objects.filter(status=status).select_related(
            'user', 'coords', 'level', 'moderated_by'
        ).prefetch_related('images').order_by('-add_time')

    @staticmethod
    def update_status(
            pass_id: int,
            new_status: str,
            moderator_id: int = None,
            comment: str = None
    ) -> tuple[bool, dict, int]:
        """Обновление статуса перевала (для сотрудников ФСТР)"""
        try:
            pass_instance = Pass.objects.get(id=pass_id)

            valid_statuses = [choice[0] for choice in Pass.Status.choices]
            if new_status not in valid_statuses:
                return False, {
                    'state': 0,
                    'message': f'Недопустимый статус. Допустимые значения: {", ".join(valid_statuses)}'
                }, 400

            if new_status == Pass.Status.REJECTED and not comment:
                return False, {
                    'state': 0,
                    'message': 'При отклонении перевала необходимо указать комментарий с причиной'
                }, 400

            old_status = pass_instance.status
            pass_instance.status = new_status
            pass_instance.moderation_date = timezone.now()

            if comment:
                pass_instance.moderation_comment = comment

            if moderator_id:
                try:
                    moderator = User.objects.get(id=moderator_id)
                    pass_instance.moderated_by = moderator
                except User.DoesNotExist:
                    logger.warning(f"Модератор с id {moderator_id} не найден")

            pass_instance.save()

            logger.info(f"Статус перевала {pass_id} изменён: {old_status} -> {new_status}")

            return True, {
                'state': 1,
                'message': f'Статус перевала изменён на "{pass_instance.get_status_display()}"'
            }, 200

        except Pass.DoesNotExist:
            return False, {'state': 0, 'message': f'Перевал с id {pass_id} не найден'}, 404
        except Exception as e:
            logger.error(f"Ошибка при обновлении статуса: {str(e)}")
            return False, {'state': 0, 'message': f'Ошибка: {str(e)}'}, 500