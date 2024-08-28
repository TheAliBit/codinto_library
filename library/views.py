from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters

from .models import Book, Category, Review
from library.serializers.home_page_serializers import BookSerializer, BookDetailSerializer, ReviewSerializer
from library.serializers.category_serializers import CategorySerializer
from library.serializers.book_serializers import FullBookSerializer
from library.filters import CustomBookFilterSet, CustomReviewFilterSet

from django.db.models import Count, Q

from .serializers.review_serializers import DetailedReviewSerializer, DetailedReviewSerializer


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

    def get_serializer_class(self):
        if self.action == 'list':
            return BookSerializer
        else:
            return BookDetailSerializer


class HomePageAPIView(APIView):
    @staticmethod
    def get(request, *args, **kwargs):
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


class SearchListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = FullBookSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = CustomBookFilterSet
    filterset_fields = ['category']
    search_fields = ['title']


class BorrowRequestAPIView(APIView):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        book = get_object_or_404(Book, pk=pk)


class UserReviewListView(generics.ListAPIView):
    serializer_class = DetailedReviewSerializer
    filterset_class = CustomReviewFilterSet

    def get_queryset(self):
        user = self.request.user
        queryset = Review.objects.filter(user=user)
        return queryset.order_by('-created_at')


class UserReveiwDetailView(generics.RetrieveAPIView, DestroyAPIView, UpdateAPIView):
    serializer_class = DetailedReviewSerializer

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(user=user)







