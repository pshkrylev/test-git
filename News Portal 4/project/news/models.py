from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='CategorySubscriber', related_name='subscribed_categories')

    def __str__(self):
        return self.name


class CategorySubscriber(models.Model):
    """Промежуточная модель для подписчиков категории"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'category')

    def __str__(self):
        return f"{self.user.username} подписан на {self.category.name}"


class Post(models.Model):
    # ... существующие поля ...
    categories = models.ManyToManyField(Category, through='PostCategory', related_name='posts')

    # ... остальные поля и методы ...