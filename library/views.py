from django.db.models import Count, Q
from django.utils import timezone

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import DestroyAPIView, UpdateAPIView, RetrieveAPIView, CreateAPIView, \
    get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from library.filters import CustomBookFilterSet, CustomBorrowHistoryFilter
from library.serializers.book_serializers import FullBookSerializer, SingleBookUserSerializer
from library.serializers.category_serializers import CategorySerializer, SimpleCategoryListSerializer, \
    SingleCategorySerializer
from library.serializers.home_page_serializers import BookSerializer, BookSerializerForAdmin, \
    BookListSerializerForAdmin, BookAvailableRemainderSerializer
from .models import Book, Category, ReviewRequest, BorrowRequest, ExtensionRequest, BaseRequestModel, Notification, \
    ReturnRequest
from .serializers.Request_serializers import UserRequestSerializer, \
    UserBorrowRequestSerializer, UserExtensionRequestSerializer, UserReturnRequestSerializer, BaseRequestSerializer
from .serializers.admin_serializers import AdminRequestSerializer, AdminNotificationSerializer, BorrowHistorySerializer
from .serializers.notif_serializerss import UserNotificationSerializer
from .serializers.review_serializers import DetailedReviewSerializer, ReviewsSerializerForBooks
from .serializers.user_serializers import UserCreateReviewSerializer


class CategoryView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.order_by('id')
    serializer_class = CategorySerializer
    filterset_fields = ['parent']

    def get_queryset(self):
        queryset = super().get_queryset()
        parent_param = self.request.query_params.get('parent', None)
        if parent_param is None:
            queryset = queryset.filter(parent__isnull=True)
        return queryset.prefetch_related('children')


class SimpleCategoryList(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.order_by('id')
    serializer_class = SimpleCategoryListSerializer
    filterset_fields = ['parent']


class SingleCategoryView(RetrieveAPIView, DestroyAPIView, UpdateAPIView):
    serializer_class = SingleCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cateogry_id = self.kwargs.get('pk')
        category = get_object_or_404(Category, pk=cateogry_id)
        return Category.objects.get(category=category)


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.order_by('id')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class DetailedBookView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = SingleBookUserSerializer
    permission_classes = [IsAuthenticated]


class HomePageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, *args, **kwargs):
        newest_books = Book.objects.order_by('-created_at')[:10]
        newest_books_data = BookSerializer(newest_books, many=True).data

        most_popular_books = Book.objects.annotate(
            borrow_requests_count=Count('requests', filter=Q(
                requests__borrowrequest__isnull=False)),
        ).order_by('-borrow_requests_count', )[:10]
        most_popular_books_data = BookSerializer(
            most_popular_books, many=True).data
        most_reviewed_books = Book.objects.annotate(
            review_requests_count=Count('requests', filter=Q(
                requests__reviewrequest__isnull=False)),
        ).order_by('-review_requests_count')[:10]
        most_reviewed_books_data = BookSerializer(
            most_reviewed_books, many=True).data

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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = ReviewRequest.objects.filter(user=user)
        return queryset.order_by('-created_at')


class UserReviewDetailView(generics.RetrieveAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    serializer_class = DetailedReviewSerializer
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = BaseRequestModel.objects.filter(user=user)
        return queryset.order_by('created_at')


class UserBorrowRequestView(CreateAPIView):
    serializer_class = UserBorrowRequestSerializer
    permission_classes = [IsAuthenticated]
    queryset = BaseRequestModel.objects.all()

    def perform_create(self, serializer):
        book_id = self.kwargs.get('pk')
        book = get_object_or_404(Book, pk=book_id)
        has_pending_request = BaseRequestModel.objects.filter(
            user=self.request.user,
            book=book,
            status='pending'
        ).exists()
        if has_pending_request:
            raise ValidationError("! شما یک در خواست در حال بررسی دارید")
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
    permission_classes = [IsAuthenticated]
    queryset = BaseRequestModel.objects.all()

    def perform_create(self, serializer):
        book_id = self.kwargs.get('pk')
        book = get_object_or_404(Book, pk=book_id)
        has_pending_request = BaseRequestModel.objects.filter(
            user=self.request.user,
            book=book,
            status='pending'
        ).exists()
        if has_pending_request:
            raise ValidationError("! شما یک درخواست در حال بررسی دارید")
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
    permission_classes = [IsAuthenticated]
    queryset = BaseRequestModel.objects.all()

    def perform_create(self, serializer):
        book_id = self.kwargs.get('pk')
        book = get_object_or_404(Book, pk=book_id)
        score = serializer.validated_data.pop('score', None)
        description = serializer.validated_data.pop('description', None)

        ReviewRequest.objects.create(
            score=score,
            description=description,
            user=self.request.user,
            type='review',
            book=book,
            status='pending'
        )

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
    permission_classes = [IsAuthenticated, IsAdminUser]
    search_fields = ['status']

    def get_queryset(self):
        queryset = BaseRequestModel.objects.select_related('user', 'book', 'borrowrequest', 'extensionrequest',
                                                           'returnrequest', 'reviewrequest').all()
        return queryset.order_by('-created_at')


class AdminSingleRequestView(RetrieveAPIView, UpdateAPIView):
    serializer_class = AdminRequestSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

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
        # self.send_sms_notification(instance)
        self.create_notification(instance)

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
            raise ValidationError(
                "نسخه ای از این کتاب در حال حاظر موجود نمی باشد")

    def handle_extension_request(self, request):
        extension_request = ExtensionRequest.objects.get(id=request.id)
        extension_request.extend_duration(self.request)

    def handle_return_request(self, request):
        return_request = ReturnRequest.objects.get(id=request.id)
        user = return_request.user
        book = return_request.book
        book.count += 1
        book.save()
        borrow_request = BorrowRequest.objects.filter(
            user=user, book=book).last()
        borrow_request.end_date = timezone.now()
        borrow_request.is_finished = True
        borrow_request.save()

    def handle_rejection(self, request):
        # I added here for myself, it's not important
        pass

    def create_notification(self, request):
        title = f"درخواست {request.type} شما توسط ادمین {request.status}"
        description = f"درخواست {request.type} شما برای کتاب {request.book.title} توسط ادمین {request.status}"

        Notification.objects.create(
            user=request.user,
            book=request.book,
            title=title,
            description=description,
            type='request'
        )


class AdminBookView(ListAPIView, CreateAPIView):
    serializer_class = BookListSerializerForAdmin
    permission_classes = [IsAuthenticated, IsAdminUser]
    search_fields = ['title']

    def get_queryset(self):
        queryset = Book.objects.select_related(
            'category__parent__parent').all()
        return queryset.order_by('-created_at')


class AdminSingleBookView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    serializer_class = BookSerializerForAdmin
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return Book.objects.all()


class UserMyBookView(ListAPIView):
    serializer_class = BaseRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BaseRequestModel.objects.filter(user=self.request.user, status='accepted', type='borrow')


class UserNotificationList(ListAPIView):
    serializer_class = UserNotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)

    # filterset_class = CustomPublicNotificationsFilter

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(
            Q(user=user) or Q(user__is_superuser=True)
        ).exclude(Q(title="")).order_by('-created_at')


class AdminNotificationView(ListAPIView, CreateAPIView):
    serializer_class = AdminNotificationSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
            response_data = {
                'message': ".درخواست موجود شد به من اطلاع بده با موفقیت ایجاد شد"
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BorrowHistoryView(ListAPIView):
    serializer_class = BorrowHistorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomBorrowHistoryFilter

    def get_queryset(self):
        return BorrowRequest.objects.filter(status='accepted')


class BookReviewsForUser(ListAPIView):
    serializer_class = ReviewsSerializerForBooks
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        book_id = self.kwargs.get('pk')
        return ReviewRequest.objects.filter(book_id=book_id, status='accepted').order_by('-created_at')


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'list':
            return SimpleCategoryListSerializer
        elif self.action == 'nested':
            return CategorySerializer
        return SimpleCategoryListSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='nested')
    def nested(self, request):
        categories = Category.objects.filter(parent=None)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)
