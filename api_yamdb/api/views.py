from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.filters import TitleFilters
from api.permissions import (IsAdminPermission, IsModeratorPermission,
                             IsUserPermission, ReadOrAdminPermission,
                             ReadOrUserPermission)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleCreateSerializer, TitleSerializer)
from review.models import Category, Comment, Genre, Review, Title


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
    lookup_field = 'slug'
    permission_classes = (ReadOrAdminPermission, )
    pagination_class = LimitOffsetPagination
    queryset = Category.objects.all()


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
    filter_backends = (DjangoFilterBackend,)
    filter_class = TitleFilters
    permission_classes = [ReadOrAdminPermission]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return TitleSerializer
        return TitleCreateSerializer


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
