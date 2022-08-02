from datetime import datetime

from django.http import QueryDict

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from review.models import Comment, Review, Category, Genre, Title, GenreTitle


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )
    year = serializers.IntegerField()

    def validate_year(self, value):
        year = datetime.today().year
        if value > year:
            raise serializers.ValidationError(
                'Проверьте год произведения'
            )
        return value

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField(method_name='get_rating')

    def get_rating(self, instance):
        if instance.rating == 0:
            instance.rating = None
            return instance.rating
        return instance.rating

    class Meta:
        fields = '__all__'
        # fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'rating', 'pub_date')

    validators = [
        UniqueTogetherValidator(
            queryset=Review.objects.all(),
            fields=['title', 'author']
        )]

    def validate(self, data):
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')

        if (
            self.context.get('request').method == 'POST'
            and Review.objects.filter(
                title_id=title_id, author_id=author.id
            ).exists()
        ):
            raise serializers.ValidationError(
                'Вы уже оставляли свой отзыв на данное произведение'
            )
        return data

    def validate_rating(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError('Неверная оценка')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = serializers.SlugRelatedField(slug_field='text', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
