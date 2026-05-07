from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import EmailConfirmationToken

User = get_user_model()


class AccountsTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(username='testuser', email='test@test.com', password='12345')
        self.assertEqual(user.username, 'testuser')
        self.assertFalse(user.is_verified)

    def test_token_creation(self):
        user = User.objects.create_user(username='testuser2', email='test2@test.com', password='12345')
        token = EmailConfirmationToken.objects.create(user=user)
        self.assertIsNotNone(token.token)
        self.assertEqual(len(token.token), 43)