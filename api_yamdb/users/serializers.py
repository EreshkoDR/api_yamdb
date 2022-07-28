from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User, VerificationEmailKey


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


class AuthTokenSerializer(serializers.Serializer):
    """Сериализатор получения токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField(max_length=64)

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
        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
