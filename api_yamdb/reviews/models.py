from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(
        'Название категории', max_length=200
    )
    slug = models.SlugField(
        'Слаг категории', unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        'Название жанра', max_length=200
    )
    slug = models.SlugField(
        'Слаг жанра', unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Название', max_length=200
    )
    year = models.DateTimeField(
        'Год выпуска', auto_now_add=True
    )
    rating = models.IntegerField(
        blank=True, default=0
    )
    description = models.TextField(
        'Описание', blank=True
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
