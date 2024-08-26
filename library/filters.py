from django.db.models import Q, Count
from django_filters import rest_framework as filters
from library.models import Book


class CustomBookFilterSet(filters.FilterSet):
    filter_type = filters.ChoiceFilter(
        method='filter_by_type',
        choices=[('latest', 'تازه ترین ها'), ('popular', 'پرطرفدار ها'), ('most_popular', 'محبوب ترین ها')],
        label='مرتب سازی'
    )

    class Meta:
        model = Book
        fields = ['category', 'filter_type']

    def filter_by_type(self, queryset, name, value):
        if value == 'latest':
            return queryset.order_by('-created_at')[:10]
        elif value == 'popular':
            return queryset.annotate(
                borrow_requests_count=Count('requests', filter=Q(requests__borrowrequest__isnull=False)),
            ).order_by('-borrow_requests_count')[:10]
        elif value == 'most_popular':
            return queryset.annotate(
                review_requests_count=Count('requests', filter=Q(requests__reviewrequest__isnull=False)),
            ).order_by('-review_requests_count')[:10]
        return queryset
