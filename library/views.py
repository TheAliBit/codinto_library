from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, mixins, generics
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets

from .models import Book, Category, BorrowRequest
from library.serializers.main_page_serializers import BookSerializer
from library.serializers.category_serializers import CategorySerializer
from core.serializers.profile_serializers import ProfileSerializer
from library.serializers.book_serializers import FullBookSerializer

from django.db.models import Count, Q


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


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.order_by('id')
    serializer_class = BookSerializer


# class MainPageAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         newest_books = Book.objects.order_by('created_at')[:10]
#         newest_books_data = BookSerializer(newest_books, many=True).data
#
#         most_popular_books = Book.objects.order_by()
#         most_popular_books_data = BookSerializer(most_popular_books, many=True).data
#
#         most_reviewed_books = Book.objects.order_by()
#         most_reviewed_books_data = BookSerializer(most_reviewed_books, many=True).data
#
#         data = {
#             'newest_books': newest_books_data
#         }
#
#         return Response(data, status=status.HTTP_200_OK)

class HomePageAPIView(APIView):
    def get(self, request, *args, **kwargs):
        newest_books = Book.objects.order_by('-created_at')[:10]
        newest_books_data = BookSerializer(newest_books, many=True).data

        most_popular_books = Book.objects.annotate(
            borrow_requests_count=Count('requests', filter=Q(requests__borrowrequest__isnull=False)),
        ).order_by('-borrow_requests_count', )[:10]
        most_popular_books_data = BookSerializer(most_popular_books, many=True).data

        most_reviewed_books = Book.objects.annotate(
            review_requests_count=Count('requests', filter=Q(requests__reviewrequest__isnull=False)),
        ).order_by('-review_requests_count')[:10]
        most_reviewed_books_data = BookSerializer(most_reviewed_books, many=True).data

        data = {
            'تازه ترین ها': newest_books_data,
            'پرطرفدار ها': most_popular_books_data,
            'محبوب ترین ها': most_reviewed_books_data,
        }

        return Response(data, status=status.HTTP_200_OK)


class SearchPageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response(serializer.data)
