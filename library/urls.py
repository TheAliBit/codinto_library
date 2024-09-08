from django.urls import path
from rest_framework.routers import DefaultRouter

from library.views import CategoryViewSet, HomePageAPIView, BookViewSet, SearchListAPIView, UserReviewListView, \
    UserReveiwDetailView, DetailedBookView, RequestsListView, UserBorrowRequestView, AdminRequestView, \
    AdminSingleRequestView, AdminBookView, AdminSingleBookView

router = DefaultRouter()

urlpatterns = [
                  path('user/home/', HomePageAPIView.as_view(), name='home'),
                  path('user/search/', SearchListAPIView.as_view(), name='search'),
                  path('user/category/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
                  path('user/reviews/', UserReviewListView.as_view(), name='review-detail'),
                  path('user/reviews/<int:pk>/', UserReveiwDetailView.as_view(), name='review-detail'),
                  path('user/books/', BookViewSet.as_view({'get': 'list'}), name='book-list'),
                  path('user/books/<int:pk>/', DetailedBookView.as_view(), name='book-detail'),
                  path('user/books/<int:pk>/borrow/', UserBorrowRequestView.as_view(), name='user-requests'),
                  path('user/requests/', RequestsListView.as_view(), name='request-list'),
                  path('super-user/requests/', AdminRequestView.as_view(), name='admin-request'),
                  path('super-user/requests/<int:pk>/', AdminSingleRequestView.as_view(), name='admin-single-request'),
                  path('super-user/books/', AdminBookView.as_view(), name='admin-book'),
                  path('super-user/books/<int:pk>/', AdminSingleBookView.as_view(), name='admin-single-request'),
              ] + router.urls
