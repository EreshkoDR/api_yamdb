from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(
    'categories', CategoryViewSet, basename='categories'
)
router_v1.register(
    'genres', GenreViewSet, basename='genres'
)
router_v1.register('titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
