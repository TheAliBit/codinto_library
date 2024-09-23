from django.db.models import Q, Count
from django.utils import timezone
from django_filters import rest_framework as filters

from library.models import Book, ReviewRequest, Notification, BorrowRequest, Category


class CustomBookFilterSet(filters.FilterSet):
    is_available = filters.BooleanFilter(method='is_available_filter', label='فقط موجود ها')
    filter_type = filters.ChoiceFilter(
        method='filter_by_type',
        choices=[('latest', 'تازه ترین ها'), ('popular', 'پرطرفدار ها'), ('most_popular', 'محبوب ترین ها')],
        label='مرتب سازی'
    )
    category = filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        field_name='category',
        conjoined=False,
        label="دسته بندی"
    )

    class Meta:
        model = Book
        fields = ['category', 'filter_type']

    def is_available_filter(self, queryset, name, value):
        if value == True:
            return queryset.filter(count__gt=0)
        else:
            return queryset.filter(count=0)

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


class CustomReviewFilterSet(filters.FilterSet):
    start_date = filters.DateFilter(field_name='created_at', lookup_expr='gte', label='زمان شروع')
    end_date = filters.DateFilter(field_name='created_at', lookup_expr='lte', label='زمان پایان')

    class Meta:
        model = ReviewRequest
        fields = ['start_date', 'end_date']


class CustomPublicNotificationsFilter(filters.FilterSet):
    is_superuser = filters.BooleanFilter(method='filter_is_superuser', label='اطلاع رسانی عمومی')

    class Meta:
        model = Notification
        fields = []

    def filter_is_superuser(self, queryset, name, value):
        if value:
            return queryset.filter(user__is_superuser=True)
        return queryset


class CustomBorrowHistoryFilter(filters.FilterSet):
    is_finished = filters.BooleanFilter(method='filter_is_finished', label="مطالعه شده")

    class Meta:
        model = BorrowRequest
        fields = []

    def filter_is_finished(self, queryset, name, value):
        now = timezone.now()
        if value:
            return queryset.filter(end_date__lt=now)
        else:
            return queryset.filter(end_date__gt=now)
