from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins

# from users.models import User
from users.serializers import AuthTokenSerializer, ConfirmationCodeSerializer


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
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthTokenViewSet(CreateModelViewSet):
    """Вьюсет получения токена."""
    serializer_class = AuthTokenSerializer
    authentication_classes = []
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        token = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


# class UserViewSet(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     pagination_class = LimitOffsetPagination
