# Описание
Проект API для YaMDB - собирает отзывы пользователей на различные произведения

### Технологии
Hазрабатан на фреймворке Django 2.2.16 и DRF 3.12.4


### Развертка и запуск проекта

#### Клонирование репозитория
Клонировать репозиторий и перейти в него в командной строке:

    git@github.com:EreshkoDR/api_yamdb.git
    cd api_yamdb
#### Виртуальное окружение
Cоздать виртуальное окружение:

`Mac/Linux`

    python3 -m venv env
`Windows`
    
    python -m venv venv
Активация окружения

`Mac/Linux`

    source venv/bin/activate
`Windows`

    source venv/Script/activate
#### Установка зависимостей проекта
Установить зависимости из файла requirements.txt:

`Mac/Linux`

    python3 -m pip install --upgrade pip
    pip install -r requirements.txt
`Windows`

    python -m pip install --upgrade pip
    pip install -r requirements.txt

#### Миграции проекта
Перейти в каталог api_yamdb:

    cd api_yamdb
Выполнить миграции:

`Mac/Linux`

    python3 manage.py migrate
`Windows`

    python manage.py migrate
Запустить проект:

`Mac/Linux`

    python3 manage.py runserver
`Windows`

    python3 manage.py runserver
    
### API
Документация API доступна по следующему эндпоинту:

    http://127.0.0.1:8000/redoc

#### Регистрация
Для регистрации отправьте POST-запрос на эндпоит `api/v1/auth/signup/`, в теле запроса укажите:
```JSON
{
    "username": "your_username",
    "email": "your_email"
}
```
При успешной регистрации сервер вернет данные с кодом 200.
Далее ~~на указанный электронный адрес~~ в папке sent_emails директории проекта будет лог-файл эмитирующий электронное письмо. В нем указан верификационный ключ, его необходимо сохранить для дальнейшего получения JWT-токена
#### Получение JWT-токена
Для получения JWT-токена, отправьте POST-запрос на эндпоит `api/v1/auth/token/`, в теле запроса укажите:
```JSON
{
    "username": "your_username",
    "confirmation_code": "your_code"
}
```
на энипоинт:

В ответ API вернёт JWT-токен
~~~JSON
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjIwODU1Mzc3LCJqdGkiOiJkY2EwNmRiYTEzNWQ0ZjNiODdiZmQ3YzU2Y2ZjNGE0YiIsInVzZXJfaWQiOjF9.eZfkpeNVfKLzBY7U0h5gMdTwUnGP3LjRn5g8EIvWlVg"
}
~~~

`token` - Сам JWT-токен
Токен используется в заголовке запроса под ключом `Bearer`


## Авторы

### Данил Ерешко 
##### Управление пользователями, системы регистрации и аутентификации
##### Системы верификации через e-mail

### Василий Вигилянский 
##### Категории, жанры, произведения
##### Создание моделей, представлений

### Екатерина Садыкова 
##### Отзывы, комментарии, рейтинги
##### Создание моделей, представлений, определения прав доступа
