from django_filters import rest_framework

from reviews.models import Title


class TitleFilter(rest_framework.FilterSet):
    category = rest_framework.CharFilter(field_name='category__slug',
                                         lookup_expr='contains')
    genre = rest_framework.CharFilter(field_name='genre__slug',
                                      lookup_expr='contains')
    name = rest_framework.CharFilter(field_name='name',
                                     lookup_expr='contains')
    year = rest_framework.CharFilter(field_name='year')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']
