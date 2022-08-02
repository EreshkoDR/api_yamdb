from hashlib import sha256

from django.core.mail import send_mail

from api_yamdb.settings import SECRET_KEY
from .models import VerificationEmailKey


def get_key():
    """Генерация ключа по sha256."""
    # key = ''.join(choice(ascii_lowercase) for _ in range(24))
    key = SECRET_KEY
    return sha256(key.encode()).hexdigest()


def send_code(user):
    """
    Функция добавляет в БД данные о пользователе и ключе,
    затем отправляет на электронную почту сообщение с ключом.
    """
    key = get_key()
    VerificationEmailKey.objects.update_or_create(user=user, key=key)
    send_mail(
        subject='Your verification key',
        message=f'Hi! your key:\n{key}',
        from_email='verify@mail.com',
        recipient_list=[user.email],
    )
