from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Category, CategorySubscriber


class SubscribeToCategoryView(LoginRequiredMixin, View):
    """Представление для подписки на категорию"""

    def post(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)

        # Проверяем, не подписан ли уже пользователь
        if CategorySubscriber.objects.filter(user=request.user, category=category).exists():
            messages.warning(request, f'Вы уже подписаны на категорию "{category.name}"')
        else:
            CategorySubscriber.objects.create(user=request.user, category=category)
            messages.success(request, f'Вы успешно подписались на категорию "{category.name}"')

        return redirect(request.META.get('HTTP_REFERER', 'news_list'))


class UnsubscribeFromCategoryView(LoginRequiredMixin, View):
    """Представление для отписки от категории"""

    def post(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)

        deleted_count, _ = CategorySubscriber.objects.filter(
            user=request.user,
            category=category
        ).delete()

        if deleted_count:
            messages.success(request, f'Вы отписались от категории "{category.name}"')
        else:
            messages.warning(request, f'Вы не были подписаны на категорию "{category.name}"')

        return redirect(request.META.get('HTTP_REFERER', 'news_list'))