from rest_framework import generics
from django.db.models import Count
from .models import Book
from library.serializers.main_page_serializers import BookSerializer


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
