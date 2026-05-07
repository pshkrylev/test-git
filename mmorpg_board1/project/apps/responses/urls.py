from django.urls import path
from . import views

app_name = 'responses'

urlpatterns = [
    # Мои отклики (приватная страница)
    path('my/', views.my_responses, name='my_responses'),

    # Создание отклика на объявление
    path('create/<int:post_pk>/', views.response_create, name='response_create'),

    # Принятие отклика
    path('accept/<int:pk>/', views.accept_response, name='accept_response'),

    # Удаление отклика
    path('delete/<int:pk>/', views.delete_response, name='delete_response'),
]