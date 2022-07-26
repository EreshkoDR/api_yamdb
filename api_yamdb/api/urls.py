# импорт вьюшек
from django.urls import include, path
from rest_framework import routers

router_v1 = routers.DefaultRouter()

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    # Добавил эндпониты аутентификации
    path('v1/auth/', include('users.urls')),
]
