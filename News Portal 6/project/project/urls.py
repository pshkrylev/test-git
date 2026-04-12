from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # allauth URL-ы
    path('', include('news.urls')),  # URL-ы приложения news
]