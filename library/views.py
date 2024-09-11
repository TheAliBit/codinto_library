from itertools import chain

from django.db.models import Count, Q
from django.template.context_processors import request
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import DestroyAPIView, UpdateAPIView, RetrieveAPIView, CreateAPIView, \
    get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from library.filters import CustomBookFilterSet
from library.serializers.book_serializers import FullBookSerializer
from library.serializers.category_serializers import CategorySerializer
from library.serializers.home_page_serializers import BookSerializer, BookSerializerForAdmin, BookListSerializerForAdmin
from .models import Book, Category, Review, BorrowRequest, ExtensionRequest, BaseRequestModel, Notification
from .serializers.Request_serializers import UserRequestSerializer, \
    UserBorrowRequestSerializer, UserExtensionRequestSerializer, UserReturnRequestSerializer, BaseRequestSerializer
from .serializers.admin_serializers import AdminRequestSerializer
from .serializers.notif_serializerss import UserNotificationSerializer
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
    serializer_class = UserBorrowRequestSerializer

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


class UserExtensionRequestView(CreateAPIView):
    serializer_class = UserExtensionRequestSerializer

    def perform_create(self, serializer):
        book_id = self.kwargs.get('pk')
        book = get_object_or_404(Book, pk=book_id)
        serializer.save(
            book=book,
            user=self.request.user,
            status='pending',
            type='extension'
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserReturnRequestView(CreateAPIView):
    serializer_class = UserReturnRequestSerializer

    def perform_create(self, serializer):
        book_id = self.kwargs.get('pk')
        book = get_object_or_404(Book, pk=book_id)
        serializer.save(
            book=book,
            user=self.request.user,
            status='pending',
            type='return'
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

    def perform_update(self, serializer):
        instance = self.get_object()
        old_status = instance.status
        new_instance = serializer.save()
        new_status = new_instance.status

        if old_status != 'accepted' and new_status == 'accepted':
            self.calculate_duration(new_instance)
        elif old_status == 'accepted' and new_status == 'accepted' or new_status == 'rejected':
            raise ValidationError(
                "! شما یک بار وضعیت در خواست را رد و یا تایید کردید و دیگر این امکان برای شما فراهم نیست")

    def calculate_duration(self, request):
        if request.type == 'borrow':
            # Check if the book is available
            book = Book.objects.filter(id=request.book_id).first()
            if book and book.count > 0:
                # Calculate borrow duration and reduce book count
                borrow_request = BorrowRequest.objects.get(id=request.id)
                borrow_request.calculate_duration(self.request)
                book.count -= 1
                book.save()
            else:
                raise ValidationError("! نسخه ای از این کتاب در حال حاظر موجود نمی باشد")
        elif request.type == 'extension':
            # Handle extension request logic
            extension_request = ExtensionRequest.objects.get(id=request.id)
            extension_request.extend_duration(self.request)


class AdminBookView(ListAPIView, CreateAPIView):
    serializer_class = BookListSerializerForAdmin
    search_fields = ['title']

    def get_queryset(self):
        queryset = Book.objects.all()
        return queryset.order_by('-created_at')


class AdminSingleBookView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    serializer_class = BookSerializerForAdmin

    def get_queryset(self):
        return Book.objects.all()


class UserMyBookView(ListAPIView):
    serializer_class = BaseRequestSerializer

    def get_queryset(self):
        return BaseRequestModel.objects.filter(user=self.request.user, status='accepted', type='borrow')


class UserNotificationList(ListAPIView):
    serializer_class = UserNotificationSerializer

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(user=user)
