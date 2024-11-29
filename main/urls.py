from django.urls import path
from .views import NewsListAPIView, NewsDetailAPIView

urlpatterns = [
    path('news/', NewsListAPIView.as_view(), name='news-list'),
    path('news/<slug:slug>/', NewsDetailAPIView.as_view(), name='news_detail'),
]
