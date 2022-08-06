from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.models import Category, Genre, Review, Title

from .filters import TitleFilter
from .permissions import CommmentAndReviewPermission, ReadOrAdminPermission
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleSerializer)
from .utils import ListCreateDestroyMixins


class CategoryViewSet(ListCreateDestroyMixins):
    """
    Представление модели Category.
    Для GET-запросов доступ для всех.
    Для POST-, DELETE-запросов доступ для администратора.
    Возможен поиск по названию.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyMixins):
    """
    Представление модели Genre.
    Для GET-запросов доступ для всех.
    Для POST-, DELETE-запросов доступ для администратора.
    Возможен поиск по названию.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """
    Представление модели Title.
    Для GET-запросов доступ для всех.
    Для POST-, DELETE- и PATCH-запросов доступ для администратора.
    Возможна фильрация по: slug категории, slug жанра, name, year.
    """
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = [ReadOrAdminPermission]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Title.objects.annotate(_rating=Avg('reviews__score'))

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return TitleSerializer
        return TitleCreateSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    Настройки доступа к Комментариям и Отзывам:
    полный доступ для автора, администратора, суперюзера
    право на удаление и частичное изменение у модератора
    только чтение у гостя и зарегистрированного пользователя.
    """
    serializer_class = CommentSerializer
    permission_classes = (CommmentAndReviewPermission,
                          IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (CommmentAndReviewPermission,
                          IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
