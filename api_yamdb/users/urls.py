from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ConfirmationViewSet, TokenView, UserViewSet

router_v1 = DefaultRouter()
router_v1.register(r'auth/signup', ConfirmationViewSet, basename='conf')
router_v1.register(r'auth/token', TokenView, basename='auth_token')
router_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router_v1.urls)),
]
