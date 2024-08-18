from rest_framework import generics
from django.db.models import Count
from .models import Book, Category, ReviewRequest
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


class NewestBooksView(generics.ListAPIView):
    queryset = Book.objects.all().order_by('created_at')[:10]
    serializer_class = BookSerializer


class MostPopularBooksView(generics.ListAPIView):
    queryset = Book.objects.all().order_by('reviews__score')[:10]
    serializer_class = BookSerializer


class MostReviewedBooksView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.annotate(review_count=Count('reviews')).order_by('-review_count')[:10]
