from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Category, Post

User = get_user_model()


class PostsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='author', password='12345')
        self.category = Category.objects.create(name='tanks')
        self.post = Post.objects.create(
            author=self.user,
            category=self.category,
            title='Test Post',
            content='Test content'
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author.username, 'author')

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Танки')