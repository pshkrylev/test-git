from django.urls import path
from . import views

urlpatterns = [
    # ... существующие URL-ы ...

    # Подписка на категории
    path('category/<int:category_id>/subscribe/',
         views.SubscribeToCategoryView.as_view(),
         name='subscribe_category'),
    path('category/<int:category_id>/unsubscribe/',
         views.UnsubscribeFromCategoryView.as_view(),
         name='unsubscribe_category'),
]