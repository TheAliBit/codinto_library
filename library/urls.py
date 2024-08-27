from django.urls import path
from rest_framework.routers import DefaultRouter

from library.views import CategoryViewSet, HomePageAPIView, BookViewSet, SearchListAPIView, UserReviewListView

router = DefaultRouter()
router.register('book-list', BookViewSet, basename='book-list')

urlpatterns = [
                  path('home/', HomePageAPIView.as_view(), name='صفحه اصلی سامانه'),
                  path('search/', SearchListAPIView.as_view(), name='صفحه جست و جو سامانه'),
                  path('category/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
                  path('my-reviews/', UserReviewListView.as_view(), name='review-detail'),
                  # path('book-list/borrow/', BorrowRequest)
              ] + router.urls
