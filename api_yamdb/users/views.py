from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins

from api.permissions import IsAdminPermission, IsUserPermission
from users.models import User
from users.serializers import (ConfirmationCodeSerializer, TokenSerializer,
                               UserMeSerializer, UserSerializer)
from users.verifications import send_code


class CreateModelViewSet(GenericViewSet, mixins.CreateModelMixin):
    pass


class ConfirmationViewSet(CreateModelViewSet):
    """
    ## Получения ключа верификации.
    При обращении к эндпоинту `/auth/token/` с валидными данными создается
    новый пользователь, на электронную почту отправляется
    ключ верификации, который в последующем используется для
    создаения/обновления JWT-Токена.
    """
    serializer_class = ConfirmationCodeSerializer
    authentication_classes = []
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        user = User.objects.create(username=username, email=email)
        send_code(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(CreateModelViewSet):
    """
    ## Получение токена.
    При обращении к эндпоинту `/auth/token/` с валидными данными
    создается/обновляется JWT-Токен. Токен используется для аутентификации
    и передаётся в заголовке при каждом запросе под ключом `Bearer`.
    Полученный токен можно обновить, отправив валилный запрос
    на тот же эндпоинт `/auth/token/`.
    """
    serializer_class = TokenSerializer
    authentication_classes = []
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data.get('token')
        return Response({'token': token}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """
    ## Вьюсет пользователей.
    При эндпоинте "users/me/" вызвается функция `get_me()`.
    GET-запрос возвращает информацию о пользователе.
    PATCH-запрос обновляет информацию о пользователе.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminPermission, )

    @action(
        methods=['get', "patch"], url_path='me',
        permission_classes=[IsUserPermission], detail=False)
    def get_me(self, request, pk=None):
        if request.method != 'PATCH':
            serializer = UserMeSerializer(request.user)
            return Response(serializer.data)
        instance = request.user
        serializer = UserMeSerializer(
            instance,
            data=request.data,
            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
