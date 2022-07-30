from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from review.models import Category, Comment, Genre, Review, Title

from .permissions import (IsAdminPermission, IsModeratorPermission,
                          IsUserPermission, ReadOrAdminPermission, ReadOrUserPermission)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleCreateSerializer, TitleSerializer)


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """
    Представление модели Category.
    Для GET-запросов доступ для всех.
    Для POST-, DELETE-запросов доступ для администратора.
    Возможен поиск по названию.
    """
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    # Добавил исправленный пермишин
    # изменил поле поиска при детализации с "pk" на "slug" (см. lookup_field)
    # подключил пагинацию
    # сделал костыльный метод обхода authentication_classes при
    # GET-запросе, пока думаю как сделать более грамотно
    #
    # На данный момент неверно возвращает данные, нужно исправить
    # (см. tests\test_02_category.py:82)
    #
    # upd: Исправлено см. serializers.CategorySerializer
    lookup_field = 'slug'
    permission_classes = (ReadOrAdminPermission, )
    pagination_class = LimitOffsetPagination
    queryset = Category.objects.all() # Без этого не заработает :)

    # Костыльный способ обхода аутентификации
    # def get_authenticators(self):
    #     if self.request.method == 'GET':
    #         authentication_classes = []
    #         return authentication_classes
    #     return super().get_authenticators()


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    Представление модели Genre.
    Для GET-запросов доступ для всех.
    Для POST-, DELETE-запросов доступ для администратора.
    Возможен поиск по названию.
    """
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    # Здесь то же самое что и ввьюсете категорий
    # Ошибка такая в тестах схожая, наверное нужно искать в сериализаторе
    # (см. tests\test_03_genre.py:73)
    #
    # upd: Исправлено см. serializers.GenreSerializer
    lookup_field = 'slug'
    permission_classes = (ReadOrAdminPermission, )
    pagination_class = LimitOffsetPagination
    queryset = Genre.objects.all()


class TitleViewSet(viewsets.ModelViewSet):
    """
    Представление модели Title.
    Для GET-запросов доступ для всех.
    Для POST-, DELETE- и PATCH-запросов доступ для администратора.
    Возможна фильрация по: slug категории, slug жанра, name, year.
    """
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'category__slug', 'genre__slug', 'name', 'year'
    )
    # lookup_field = 'pk'
    permission_classes = (ReadOrAdminPermission, )
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return TitleCreateSerializer
        return super().get_serializer_class()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [ReadOrUserPermission, ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
