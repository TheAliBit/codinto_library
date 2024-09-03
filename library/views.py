from itertools import chain
from rest_framework.filters import SearchFilter
from rest_framework.generics import DestroyAPIView, UpdateAPIView, RetrieveAPIView, CreateAPIView, \
    get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book, Category, Review, BorrowRequest, ExtensionRequest, BaseRequestModel
from library.serializers.home_page_serializers import BookSerializer, BookSerializerForAdmin
from library.serializers.category_serializers import CategorySerializer
from library.serializers.book_serializers import FullBookSerializer
from library.filters import CustomBookFilterSet

from django.db.models import Count, Q

from .serializers.Request_serializers import UserRequestSerializer, \
    UserBorrowRequestSerializer_
from .serializers.admin_serializers import AdminRequestSerializer
from .serializers.review_serializers import DetailedReviewSerializer


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


class DetailedBookView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = FullBookSerializer


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
            'newest_books': newest_books_data,
            'most_borrowed_books': most_popular_books_data,
            'highest_rated_books': most_reviewed_books_data,
        }

        return Response(data, status=status.HTTP_200_OK)


class SearchListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = FullBookSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = CustomBookFilterSet
    filterset_fields = ['category']
    search_fields = ['title']


class UserReviewListView(ListAPIView):
    serializer_class = DetailedReviewSerializer

    # filterset_class = CustomReviewFilterSet

    def get_queryset(self):
        user = self.request.user
        queryset = Review.objects.filter(user=user)
        return queryset.order_by('-created_at')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserReveiwDetailView(generics.RetrieveAPIView, DestroyAPIView, UpdateAPIView):
    serializer_class = DetailedReviewSerializer

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(user=user)


class RequestsListView(generics.ListAPIView):
    serializer_class = UserRequestSerializer

    def get_queryset(self):
        user = self.request.user
        borrow_requests = BorrowRequest.objects.filter(user=user)
        extension_requests = ExtensionRequest.objects.filter(user=user)
        review_requests = Review.objects.filter(user=user)
        combined_queryset = list(chain(borrow_requests, extension_requests, review_requests))
        combined_queryset.sort(key=lambda x: x.created_at, reverse=True)
        return combined_queryset


class UserBorrowRequestView(CreateAPIView):
    serializer_class = UserBorrowRequestSerializer_

    def perform_create(self, serializer):
        book_id = self.kwargs.get('pk')
        book = get_object_or_404(Book, pk=book_id)
        serializer.save(
            book=book,
            user=self.request.user,
            status='pending',
            type='borrow'
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminRequestView(ListAPIView):
    serializer_class = AdminRequestSerializer
    search_fields = ['status']

    def get_queryset(self):
        queryset = BaseRequestModel.objects.all()
        return queryset.order_by('-created_at')


class AdminSingleRequestView(RetrieveAPIView, UpdateAPIView):
    serializer_class = AdminRequestSerializer

    def get_queryset(self):
        return BaseRequestModel.objects.all()


class AdminBookView(ListAPIView):
    serializer_class = BookSerializer
    search_fields = ['title']

    def get_queryset(self):
        queryset = Book.objects.all()
        return queryset.order_by('-created_at')


class AdminSingleBookView(RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView):
    serializer_class = BookSerializerForAdmin

    def get_queryset(self):
        return Book.objects.all()
