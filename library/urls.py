from django.urls import path
from rest_framework.routers import DefaultRouter

from library.views import CategoryViewSet, MainPageAPIView, BookViewSet

router = DefaultRouter()
router.register('book-list', BookViewSet, basename='لیست کتاب ها')

urlpatterns = [
                  path('category/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
                  path('main-page/', MainPageAPIView.as_view(), name='newest-books'),
                  # path('book/', BookViewSet.as_view(), name='کتاب')
              ] + router.urls
