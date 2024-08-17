from django.urls import path
from library.views import NewestBooksView, MostPopularBooksView, MostReviewedBooksView

urlpatterns = [
    path('books/newest/', NewestBooksView.as_view(), name='newest-books'),
    path('books/popular/', MostPopularBooksView.as_view(), name='most-popular-books'),
    path('books/reviewed/', MostReviewedBooksView.as_view(), name='most-reviewed-books'),
]
