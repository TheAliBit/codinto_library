from rest_framework.filters import BaseFilterBackend


class CustomFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter_type = request.query_params.get('filter', None)
        if filter_type == 'تازه ترین ها':
            queryset = queryset.order_by('-created_at')[:10]
        elif filter_type == 'پرطرفدار ها':
            queryset = queryset.order_by('-created_at')[:10]
        elif filter_type == 'محبوب ترین ها':
            queryset = queryset.order_by('-created_at')[:10]
        return queryset
