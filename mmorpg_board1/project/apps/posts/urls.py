from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    # Список всех объявлений (главная страница)
    path('', views.post_list, name='post_list'),

    # Детальная страница объявления
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

    # Создание нового объявления
    path('post/create/', views.post_create, name='post_create'),

    # Редактирование объявления
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),

    # Удаление объявления
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
]