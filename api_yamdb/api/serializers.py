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
        # тут проверка,что пользователь не может оставлять повторно ревью
        def validate(self,value):
            pass

class Comment(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')
    class Meta:
        model = Comment
        fields = '__all__'