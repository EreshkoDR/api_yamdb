from django.db import models
from django.db.models import UniqueConstraint
from users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        'Текст отзыва: ',
        help_text='Напишите что-нибудь сюда...')
    pub_date = models.DateTimeField('Дата публикации: ', auto_now_add=True)
    titles = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['titles', 'author'],
                                    name='uniq_review')]
class Comment(CreatedModel):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
        )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария')
    text = models.TextField(
        'Текст коментария:',
        help_text='Оставьте коментарий в поле')
    pub_date = models.DateTimeField('Дата коментария', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text[:15]