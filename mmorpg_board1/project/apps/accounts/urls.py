from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'accounts'  # Пространство имён

urlpatterns = [
    # Регистрация
    path('register/', views.register, name='register'),

    # Подтверждение email
    path('confirm/<str:token>/', views.confirm_email, name='confirm_email'),

    # Вход и выход
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='post_list'), name='logout'),
]