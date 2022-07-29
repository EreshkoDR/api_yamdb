from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from review.models import Comment, Review, Category, Genre, Title

from .permissions import (IsAdminPermission, IsModeratorPermission,
                          IsUserPermission)
from .serializers import CommentSerializer, ReviewSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets

from .serializers import CategorySerializer, GenreSerializer, TitleSerializer

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminPermission, IsModeratorPermission, IsUserPermission]
    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminPermission, IsModeratorPermission, IsUserPermission]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)



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
