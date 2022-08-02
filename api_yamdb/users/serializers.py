from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import AccessToken

from .models import User, VerificationEmailKey


class ConfirmationCodeSerializer(serializers.Serializer):
    """Сериализатор отправки кода подтверждения."""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def validate(self, attrs):
        username = attrs.get('username')
        if username.lower() == 'me':
            msg = 'Имя позователя не может быть "me".'
            raise serializers.ValidationError(msg)
        return attrs


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField(max_length=64)

    @classmethod
    def get_token(cls, user):
        return AccessToken.for_user(user)

    def validate(self, attrs):
        username = attrs.get('username')
        code = attrs.get('confirmation_code')
        if username and code:
            user = get_object_or_404(User, username=username)
            try:
                key = VerificationEmailKey.objects.get(user=user)
            except Exception:
                msg = 'Ключ недействителен'
                raise serializers.ValidationError(msg)
            if key.key != code:
                msg = 'Ключ недействителен'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Поля "username" и "confirmation_code" обязательны.'
            raise serializers.ValidationError(msg)
        user = get_object_or_404(User, username=username)
        token = self.get_token(user)
        attrs['token'] = str(token)
        return attrs


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def validate(self, attrs):
        username = attrs.get('username')
        try:
            if username.lower() == 'me':
                msg = 'Имя позователя не может быть "me".'
                raise serializers.ValidationError(msg)
        except AttributeError:
            return attrs
        return attrs

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )


class UserMeSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)
