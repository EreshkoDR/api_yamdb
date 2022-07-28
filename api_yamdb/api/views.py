from django.shortcuts import get_object_or_404
from review.models import Comment, Review
from rest_framework import filters, mixins, viewsets

from .serializers import (CommentSerializer, ReviewSerializer)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        comment = get_object_or_404(Comment, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, comment=comment)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.review