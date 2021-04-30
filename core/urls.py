from django.urls import path
from rest_framework.routers import DefaultRouter

from core.views import categories_list, get_category, get_category_news
from core.views import NewsListAPIView, NewsDetailAPIView, AuthorViewSet


router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
urlpatterns = router.urls

urlpatterns += [
    path('categories/', categories_list),
    path('categories/<int:pk>/', get_category),
    path('categories/<int:pk>/news/', get_category_news),
    path('news/', NewsListAPIView.as_view()),
    path('news/<int:pk>/', NewsDetailAPIView.as_view()),
]