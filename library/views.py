from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Book, Category
from library.serializers.main_page_serializers import BookSerializer
from library.serializers.category_serializers import CategorySerializer
from rest_framework.viewsets import ModelViewSet


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.order_by('id')
    serializer_class = CategorySerializer
    filterset_fields = ['parent']

    def get_queryset(self):
        queryset = super().get_queryset()
        parent_param = self.request.query_params.get('parent', None)
        if parent_param is None:
            queryset = queryset.filter(parent__isnull=True)
        return queryset.prefetch_related('children')


class MainPageAPIView(APIView):
    def get(self, request, *args, **kwargs):
        newest_books = Book.objects.order_by('created_at')[:10]
        newest_books_data = BookSerializer(newest_books, many=True).data

        most_popular_books = Book.objects.order_by()
        most_popular_books_data = BookSerializer(most_popular_books, many=True).data

        most_reviewed_books = Book.objects.order_by()
        most_reviewed_books_data = BookSerializer(most_reviewed_books, many=True).data

        data = {
            'newest_books': newest_books_data
        }

        return Response(data, status=status.HTTP_200_OK)
