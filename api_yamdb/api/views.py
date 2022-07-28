from rest_framework import (
    viewsets, mixins, pagination, filters
)
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Category, Genre, Title
from .serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer
)


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
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


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
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """
    Представление модели Title.
    Для GET-запросов доступ для всех.
    Для POST-, DELETE- и PATCH-запросов доступ для администратора.
    Возможна фильрация по: slug категории, slug жанра, name, year.
    """
    serializer_class = TitleSerializer
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'category__slug', 'genre__slug', 'name', 'year'
    )
