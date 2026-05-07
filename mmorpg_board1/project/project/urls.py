from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Админка Django
    path('admin/', admin.site.urls),

    # Приложение accounts (регистрация, логин, подтверждение email)
    path('', include('apps.accounts.urls')),

    # Приложение posts (объявления, категории)
    path('', include('apps.posts.urls')),

    # Приложение responses (отклики)
    path('responses/', include('apps.responses.urls')),
]

# Для разработки: раздача статических и медиа-файлов
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)