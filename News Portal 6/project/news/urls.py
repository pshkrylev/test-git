from django.contrib import admin
from django.urls import path
from news.views import test_logging

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test-logging/', test_logging, name='test_logging'),
]