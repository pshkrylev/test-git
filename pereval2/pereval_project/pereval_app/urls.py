from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    #  Создание нового перевала (Спринт 1)
    path('submitData/', views.submit_data, name='submitData'),

    #  Получение одной записи по ID (НОВЫЙ)
    path('submitData/<int:pk>/', views.get_pass, name='get_pass'),

    #  Редактирование перевала (НОВЫЙ)
    path('submitData/<int:pk>/', views.update_pass, name='update_pass'),

    #  Список всех перевалов пользователя (НОВЫЙ)
    path('submitData/', views.get_user_passes, name='get_user_passes'),

    #  Получение перевалов по статусу
    path('submitData/status/<str:status>/', views.get_passes_by_status, name='get_passes_by_status'),

    #  Обновление статуса (для ФСТР)
    path('submitData/<int:pk>/status/', views.update_pass_status, name='update_status'),
]