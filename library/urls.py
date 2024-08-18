from django.urls import path
from rest_framework.routers import DefaultRouter

from library.views import NewestBooksView, MostPopularBooksView, MostReviewedBooksView, CategoryViewSet

router = DefaultRouter()

urlpatterns = [
                  path('category/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
                  path('books/newest/', NewestBooksView.as_view(), name='newest-books'),
                  path('books/popular/', MostPopularBooksView.as_view(), name='most-popular-books'),
                  path('books/reviewed/', MostReviewedBooksView.as_view(), name='most-reviewed-books'),
              ] + router.urls
