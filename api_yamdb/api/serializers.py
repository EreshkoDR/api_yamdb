from datetime import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from review.models import Comment, Review, Category, Genre, Title, GenreTitle


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        # fields = '__all__'
        # Здесь лучше явно обозначить поля или исключить "id" т.к.
        # по документации и по тестам должно выходить быть
        # только два поля: "name" и "slug"
        #
        # Теперь тесты проходятся
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        # То же самое что и в CategorySerializer
        fields = ('name', 'slug')
        model = Genre


class TitleCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all()
    )
    year = serializers.IntegerField()

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            GenreTitle.objects.create(title=title, genre=genre)

        return title

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title

    def validate_year(self, value):
        year = datetime.today().year
        if value > year:
            raise serializers.ValidationError(
                'Проверьте год произведения'
            )
        return value


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=True
    )
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField()

    def validate_rating(self, value):
        if value == '0':
            value = None
            return value
        return value

    class Meta:
        fields = "__all__"
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
