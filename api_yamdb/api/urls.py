from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register(
    'categories', CategoryViewSet, basename='categories'
)
router_v1.register(
    'genres', GenreViewSet, basename='genres'
)
router_v1.register('titles', TitleViewSet)

router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    # Добавил эндпониты аутентификации
    path('v1/', include('users.urls')),
]
