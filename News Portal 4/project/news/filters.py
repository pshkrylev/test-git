import django_filters
from django import forms
from .models import Post, Author


class PostFilter(django_filters.FilterSet):
    # Фильтр по названию (содержит)
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название содержит'
    )

    # Фильтр по имени автора (содержит)
    author_name = django_filters.CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='Имя автора содержит'
    )

    # Фильтр по дате (позже указанной даты)
    created_at_after = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Позже даты',
        widget=forms.DateInput(attrs={'type': 'date'})  # календарь для выбора даты
    )

    class Meta:
        model = Post
        fields = ['title', 'author_name', 'created_at_after']