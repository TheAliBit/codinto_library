from random import choices

from django_filters import rest_framework as filters
from library.models import Book


class CustomBookFilterSet(filters.FilterSet):
    filter_type = filters.ChoiceFilter(
        method='filter_by_type',
        choices=[('latest', 'تازه ترین ها'), ('popular', 'پرطرفدار ها'), ('most_popular', 'محبوب ترین ها')],
        label='مرتب سازی')

    class Meta:
        model = Book
        fields = ['category', 'filter_type']

    @staticmethod
    def filter_by_type(self, queryset, name, value):
        if value == 'تازه ترین ها':
            return queryset.order_by('-created_at')[:10]
        elif value == 'پرطرفدار ها':
            return queryset.order_by('-created_at')[:10]
        elif value == 'محبوب ترین ها':
            return queryset.order_by('-created_at')[:10]
        return queryset
