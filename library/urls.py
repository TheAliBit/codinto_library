from django.urls import path
from rest_framework.routers import DefaultRouter

from library.views import CategoryViewSet, HomePageAPIView, BookViewSet

router = DefaultRouter()
router.register('book-list', BookViewSet, basename='لیست کتاب ها')

urlpatterns = [
                  path('home/', HomePageAPIView.as_view(), name='newest-books'),
                  path('category/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),

              ] + router.urls
