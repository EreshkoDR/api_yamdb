from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'Авторизированный пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    ]

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    role = models.CharField(
        "Пользовательские роли",
        choices=ROLE_CHOICES,
        default=USER,
        max_length=15,
    )


class VerificationEmailKey(models.Model):
    """Модель ключей подтверждения."""
    key = models.CharField(
        verbose_name='Key',
        max_length=64,
        primary_key=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='verification',
    )
