from django.db import models
# from django.db.models import UniqueConstraint
from django.contrib.auth 


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='review/',
        blank=True,
        null=True,
        help_text='Загрузите картинку'
    )
    text = models.TextField(
        'Текст отзыва: ',
        help_text='Напишите что-нибудь сюда...')
    pub_date = models.DateTimeField('Дата публикации: ', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='titles',
    )
    titles = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='titles',
    )

class Comment(CreatedModel):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
        )
    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name='comments',
    #     verbose_name='Автор комментария')
    text = models.TextField(
        'Текст коментария:',
        help_text='Оставьте коментарий в поле')
    created = models.DateTimeField('Дата коментария', auto_now_add=True)

    def __str__(self):
        return self.text[:15]