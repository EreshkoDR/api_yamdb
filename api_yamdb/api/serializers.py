from review.models import Comment, Review
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        model = Review
        fields = '__all__'

    validators = [UniqueTogetherValidator(
            queryset=Review.objects.all(),
            fields=['title', 'author']
        )
        ]

    def validate(self,value):
        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(
            author=author,title=title_id).exists():
            raise serializers.ValidationError('У вас уже есть отзыв на это.')
        return value

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError('Неверная оценка')
class Comment(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')
    class Meta:
        model = Comment
        fields = '__all__'