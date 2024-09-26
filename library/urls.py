from django.urls import path
from rest_framework.routers import DefaultRouter

from library.views import CategoryView, HomePageAPIView, BookViewSet, SearchListAPIView, UserReviewListView, \
    UserReviewDetailView, DetailedBookView, RequestsListView, UserBorrowRequestView, AdminRequestView, \
    AdminSingleRequestView, AdminBookView, AdminSingleBookView, UserExtensionRequestView, UserReturnRequestView, \
    UserMyBookView, UserNotificationList, AdminNotificationView, AvailableRemainderView, \
    BorrowHistoryView, BookReviewsForUser, CategoryViewSet

router = DefaultRouter()
router.register(r'category', CategoryViewSet, basename='category')

urlpatterns = [
    path('user/home/', HomePageAPIView.as_view(), name='home'),
    path('user/search/', SearchListAPIView.as_view(), name='search'),
    path('user/reviews/', UserReviewListView.as_view(), name='review-detail'),
    path('user/reviews/<int:pk>/', UserReviewDetailView.as_view(), name='review-detail'),
    path('user/books/', BookViewSet.as_view({'get': 'list'}), name='book-list'),
    path('user/books/<int:pk>/', DetailedBookView.as_view(), name='book-detail'),
    path('user/books/<int:pk>/borrow/', UserBorrowRequestView.as_view(), name='user-borrow-request'),
    path('user/requests/', RequestsListView.as_view(), name='request-list'),
    path('user/books/<int:pk>/extension/', UserExtensionRequestView.as_view(),
         name='user-extension-request'),
    path('user/books/<int:pk>/return/', UserReturnRequestView.as_view()),
    path('user/books/<int:pk>/reviews/', BookReviewsForUser.as_view(), name='user-review'),
    path('user/books/<int:pk>/available/', AvailableRemainderView.as_view(),
         name='book-available-remainder'),
    path('user/my-books/', UserMyBookView.as_view(), name='user-my-books'),
    path('user/notifications/', UserNotificationList.as_view(), name='user-notifications'),
    # super user urls
    path('super-user/requests/', AdminRequestView.as_view(), name='admin-request'),
    path('super-user/requests/<int:pk>/', AdminSingleRequestView.as_view(),
         name='admin-single-request'),
    path('super-user/books/', AdminBookView.as_view(), name='admin-book'),
    path('super-user/books/<int:pk>/', AdminSingleBookView.as_view(), name='admin-single-request'),
    path('super-user/notifications/', AdminNotificationView.as_view(), name='admin-creat-notifications'),
    path('super-user/history/',BorrowHistoryView.as_view(), name ='borrow_history'),
    # path('super-user/categories/', SimpleCategoryList.as_view(),  name='category-list'),
    # path('super-user/categories/nested-categories/', CategoryView.as_view(),  name='category-list'),
    # path('super-user/categories/<int:pk>/', SingleCategoryView.as_view(),  name='category-list'),
    # path('super-user/categories/nested-categories/<int:pk>/', SingleCategoryView.as_view(),  name='category-list'),

] + router.urls
