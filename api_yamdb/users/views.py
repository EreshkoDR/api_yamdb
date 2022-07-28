from rest_framework import filters, status, viewsets
from rest_framework.exceptions import MethodNotAllowed
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
    """Вьюсет получения ключа."""
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
    """Получение токена."""
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
    Вьюсет пользователей. При эндпоинте "users/me/" сериализатор меняется
    на UserMeSerializer, пермишены меняются на IsUserPermission.

    # Пока работает, не трогать.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminPermission, )

    def get_permissions(self):
        if self.kwargs.get('username') == 'me':
            permission_classes = [IsUserPermission]
        else:
            permission_classes = [IsAdminPermission]
        return [permission() for permission in permission_classes]

    def get_serializer(self, *args, **kwargs):
        if (
            self.kwargs.get('username') == 'me'
            and (self.action == 'partial_update' or self.action == 'update')
        ):
            serializer_class = UserMeSerializer
            kwargs.setdefault('context', self.get_serializer_context())
            return serializer_class(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    def get_object(self):
        if self.kwargs.get('username').lower() == 'me':
            return self.request.user
        return super().get_object()

    def destroy(self, request, *args, **kwargs):
        if self.kwargs.get('username').lower() == 'me':
            msg = 'Вы не можете удалить себя'
            raise MethodNotAllowed(msg)
        return super().destroy(request, *args, **kwargs)
