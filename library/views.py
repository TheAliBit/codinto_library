from itertools import chain

from django.db.models import Count, Q
from django.utils import timezone

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

from library.filters import CustomBookFilterSet, CustomBorrowHistoryFilter
from library.serializers.book_serializers import FullBookSerializer, SingleBookUserSerializer
from library.serializers.category_serializers import CategorySerializer
from library.serializers.home_page_serializers import BookSerializer, BookSerializerForAdmin, \
    BookListSerializerForAdmin, BookAvailableRemainderSerializer
from .models import Book, Category, ReviewRequest, BorrowRequest, ExtensionRequest, BaseRequestModel, Notification, \
    ReturnRequest
from .serializers.Request_serializers import UserRequestSerializer, \
    UserBorrowRequestSerializer, UserExtensionRequestSerializer, UserReturnRequestSerializer, BaseRequestSerializer
from .serializers.admin_serializers import AdminRequestSerializer, AdminNotificationSerializer, BorrowHistorySerializer
from .serializers.notif_serializerss import UserNotificationSerializer
from .serializers.review_serializers import DetailedReviewSerializer
from .serializers.user_serializers import UserCreateReviewSerializer
from .tasks import send_sms_task


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
    serializer_class = SingleBookUserSerializer


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


class UserReviewListView(generics.ListAPIView):
    serializer_class = DetailedReviewSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = ReviewRequest.objects.filter(user=user)
        return queryset.order_by('-created_at')


class UserReviewDetailView(generics.RetrieveAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    serializer_class = DetailedReviewSerializer

    def get_queryset(self):
        user = self.request.user
        return ReviewRequest.objects.filter(user=user)

    def perform_update(self, serializer):
        review = get_object_or_404(ReviewRequest, pk=self.kwargs.get('pk'))
        ReviewRequest.objects.create(
            user=self.request.user,
            book=review.book,
            description=serializer.validated_data.get('description'),
            score=serializer.validated_data.get('score'),
            status='pending',
            type='review'
        )
        review.delete()


class RequestsListView(generics.ListAPIView):
    serializer_class = UserRequestSerializer

    def get_queryset(self):
        user = self.request.user
        borrow_requests = BorrowRequest.objects.filter(user=user)
        extension_requests = ExtensionRequest.objects.filter(user=user)
        review_requests = ReviewRequest.objects.filter(user=user)
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
        instance = serializer.save()

        if instance.status not in ['accepted', 'rejected']:
            return

        if instance.status == 'accepted':
            self.handle_request(instance)
        elif instance.status == 'rejected':
            self.handle_rejection(instance)
        self.send_sms_notification(instance)

    def handle_request(self, request):
        if request.type == 'borrow':
            self.handle_borrow_request(request)
        elif request.type == 'extension':
            self.handle_extension_request(request)
        elif request.type == 'return':
            self.handle_return_request(request)

    def handle_borrow_request(self, request):
        book = Book.objects.filter(id=request.book_id).first()
        if book and book.count > 0:
            borrow_request = BorrowRequest.objects.get(id=request.id)
            borrow_request.calculate_duration(self.request)
            book.count -= 1
            book.save()
        else:
            borrow_request = BorrowRequest.objects.get(id=request.id)
            borrow_request.status = 'pending'
            borrow_request.save()
            raise ValidationError("نسخه ای از این کتاب در حال حاظر موجود نمی باشد")

    def handle_extension_request(self, request):
        extension_request = ExtensionRequest.objects.get(id=request.id)
        extension_request.extend_duration(self.request)

    def handle_return_request(self, request):
        return_request = ReturnRequest.objects.get(id=request.id)
        user = return_request.user
        book = return_request.book
        book.count += 1
        book.save()
        borrow_request = BorrowRequest.objects.get(user=user, book=book)
        borrow_request.end_date = timezone.now()
        borrow_request.save()

    def handle_rejection(self, request):
        # i added here for myself, it's not important
        pass

    def send_sms_notification(self, request):
        user_phone = request.user.phone_number
        message = self.generate_sms_message(request)
        send_sms_task.delay(user_phone, message)
        # send_sms(user_phone, message)

    def generate_sms_message(self, request):
        request_type_map = {
            'borrow': 'درخواست امانت',
            'extension': 'درخواست تمدید',
            'return': 'درخواست بازگشت',
            'review': 'درخواست ثبت نظر'
        }
        request_status_map = {
            'accepted': 'تایید شد',
            'rejected': 'رد شد'
        }
        user_name = request.user.username
        book_name = request.book.title
        request_type = request_type_map.get(request.type, 'درخواست')
        request_status = request_status_map.get(request.status, 'نامشخص')
        return f"{user_name} عزیز, {request_type} شما برای کتاب {book_name} {request_status}!"


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
    filter_backends = (DjangoFilterBackend,)

    # filterset_class = CustomPublicNotificationsFilter

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(
            Q(user=user) or Q(user__is_superuser=True)
        )


class AdminNotificationView(ListAPIView, CreateAPIView):
    serializer_class = AdminNotificationSerializer

    def get_queryset(self):
        return Notification.objects.all()

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserReviewView(CreateAPIView):
    serializer_class = UserCreateReviewSerializer

    def perform_create(self, serializer):
        book_id = self.kwargs.get('pk')
        book = get_object_or_404(Book, pk=book_id)
        serializer.save(
            book=book,
            user=self.request.user,
            status='pending',
            type='review'
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AvailableRemainderView(CreateAPIView):
    serializer_class = BookAvailableRemainderSerializer

    def perform_create(self, serializer):
        book_id = self.kwargs.get('pk')
        book = get_object_or_404(Book, pk=book_id)

        if book.count > 0:
            raise ValidationError({"message": "!موجودی کتاب هنوز صفر نشده"})

        serializer.save(
            book=book,
            user=self.request.user,
            type='available',
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BorrowHistoryView(ListAPIView):
    serializer_class = BorrowHistorySerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomBorrowHistoryFilter

    def get_queryset(self):
        return BorrowRequest.objects.filter(status='accepted')
