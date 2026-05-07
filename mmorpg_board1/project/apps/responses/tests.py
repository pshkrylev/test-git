from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.posts.models import Category, Post
from .models import Response

User = get_user_model()


class ResponsesTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='author', password='12345')
        self.responder = User.objects.create_user(username='responder', password='12345')
        self.category = Category.objects.create(name='tanks')
        self.post = Post.objects.create(
            author=self.author,
            category=self.category,
            title='Test Post',
            content='Test content'
        )

    def test_response_creation(self):
        response = Response.objects.create(
            post=self.post,
            author=self.responder,
            text='Test response'
        )
        self.assertEqual(response.text, 'Test response')
        self.assertFalse(response.is_accepted)