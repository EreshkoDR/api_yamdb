from django.core.validators import MaxValueValidator, MinValueValidator
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
        return self.slug


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
        return self.slug


class Title(models.Model):
    name = models.CharField(
        'Название', max_length=200
    )
    year = models.IntegerField(
        'Год выпуска'
    )
    description = models.TextField(
        'Описание', blank=True
    )
    genre = models.ManyToManyField(
        Genre, through='GenreTitle'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='title'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    @property
    def rating(self):
        if hasattr(self, '_rating'):
            return self._rating
        return self.reviews.aggregate(models.Avg('score'))

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}: {self.genre}'


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField(
        'Текст отзыва: ',
        help_text='Напишите что-нибудь сюда...'
    )
    pub_date = models.DateTimeField('Дата публикации: ', auto_now_add=True)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
    )
    score = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_titles_author'
            )
        ]
        ordering = ('-pub_date',)


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    text = models.TextField(
        'Текст коментария:',
        help_text='Оставьте коментарий в поле'
    )
    pub_date = models.DateTimeField(
        'Дата коментария', auto_now_add=True, db_index=True
    )
