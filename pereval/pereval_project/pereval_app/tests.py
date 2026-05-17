from django.test import TestCase
from django.urls import reverse
from .models import User, Coordinates, Level, Image, Pass
import json


class PassModelTest(TestCase):
    """Тесты для модели Pass"""

    def setUp(self):
        """Подготовка тестовых данных"""
        self.user = User.objects.create(
            email='test@test.com',
            fam='Иванов',
            name='Иван',
            otc='Иванович',
            phone='+7 999 123 45 67'
        )

        self.coords = Coordinates.objects.create(
            latitude=45.3842,
            longitude=7.1525,
            height=1200
        )

        self.level = Level.objects.create(
            winter='',
            summer='1А',
            autumn='1А',
            spring=''
        )

        self.pass_instance = Pass.objects.create(
            beauty_title='пер. ',
            title='Пхия',
            other_titles='Триев',
            connect='',
            user=self.user,
            coords=self.coords,
            level=self.level,
            status='new'
        )

    def test_pass_creation(self):
        """Тест создания перевала"""
        self.assertEqual(self.pass_instance.title, 'Пхия')
        self.assertEqual(self.pass_instance.user.email, 'test@test.com')
        self.assertEqual(self.pass_instance.status, 'new')

    def test_pass_str(self):
        """Тест строкового представления"""
        self.assertIn('Пхия', str(self.pass_instance))


class APITest(TestCase):
    """Тесты для API"""

    def setUp(self):
        self.valid_data = {
            "beauty_title": "пер. ",
            "title": "Test Pass",
            "other_titles": "Test",
            "connect": "",
            "user": {
                "email": "test@test.com",
                "fam": "Тестов",
                "name": "Тест",
                "otc": "Тестович",
                "phone": "+7 999 123 45 67"
            },
            "coords": {
                "latitude": "45.3842",
                "longitude": "7.1525",
                "height": "1200"
            },
            "level": {
                "winter": "",
                "summer": "1А",
                "autumn": "1А",
                "spring": ""
            },
            "images": [
                {"data": "base64_image_1", "title": "Photo 1"}
            ]
        }

    def test_submit_data_success(self):
        """Тест успешной отправки данных"""
        response = self.client.post(
            '/api/submitData/',
            data=json.dumps(self.valid_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 200)
        self.assertIsNotNone(data['id'])

    def test_submit_data_missing_field(self):
        """Тест отправки с отсутствующим полем"""
        invalid_data = self.valid_data.copy()
        del invalid_data['title']

        response = self.client.post(
            '/api/submitData/',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data['status'], 400)

    def test_get_pass_by_id(self):
        """Тест получения перевала по ID"""
        # Сначала создаём перевал
        create_response = self.client.post(
            '/api/submitData/',
            data=json.dumps(self.valid_data),
            content_type='application/json'
        )
        pass_id = create_response.json()['id']

        # Получаем его
        response = self.client.get(f'/api/submitData/{pass_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Test Pass')

    def test_get_passes_by_email(self):
        """Тест фильтрации по email"""
        # Создаём перевал
        self.client.post(
            '/api/submitData/',
            data=json.dumps(self.valid_data),
            content_type='application/json'
        )

        # Фильтруем по email
        response = self.client.get('/api/submitData/?user__email=test@test.com')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.json()['count'], 1)