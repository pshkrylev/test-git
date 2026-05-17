from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Основной метод submitData
    path('submitData/', views.submit_data, name='submitData'),

    # GET запрос для получения записи
    path('submitData/<int:pk>/', views.get_pass, name='get_pass'),

    # PATCH запрос для редактирования (только для статуса 'new')
    path('submitData/<int:pk>/edit/', views.update_pass, name='update_pass'),

    #  ОБНОВЛЁННЫЙ МАРШРУТ: обновление статуса с комментарием
    path('submitData/<int:pk>/status/', views.update_pass_status, name='update_status'),

    # Фильтрация по email пользователя
    path('submitData/', views.get_passes_by_user, name='get_passes_by_user'),
]