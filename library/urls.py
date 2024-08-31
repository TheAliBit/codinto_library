from django.urls import path
from rest_framework.routers import DefaultRouter

from library.views import CategoryViewSet, HomePageAPIView, BookViewSet, SearchListAPIView, UserReviewListView, \
    UserReveiwDetailView, DetailedBookView, RequestsListView, UserBorrowRequestView

router = DefaultRouter()
# router.register('book-list', BookViewSet, basename='book-list')

urlpatterns = [
                  path('home/', HomePageAPIView.as_view(), name='صفحه اصلی سامانه'),
                  path('search/', SearchListAPIView.as_view(), name='صفحه جست و جو سامانه'),
                  path('category/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
                  path('reviews/', UserReviewListView.as_view(), name='review-detail'),
                  path('reviews/<int:pk>/', UserReveiwDetailView.as_view(), name='review-detail'),
                  path('book-list/', BookViewSet.as_view({'get': 'list'}), name='book-list'),
                  path('book-list/<int:pk>/', DetailedBookView.as_view(), name='book-detail'),
                  path('book-list/<int:pk>/borrow/', UserBorrowRequestView.as_view(), name='user-requests'),
                  path('requests/', RequestsListView.as_view(), name='request-list'),

              ] + router.urls
