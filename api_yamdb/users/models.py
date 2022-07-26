from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


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
        max_length=9,
    )
