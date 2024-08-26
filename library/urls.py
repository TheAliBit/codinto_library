from django.urls import path
from rest_framework.routers import DefaultRouter

from library.views import CategoryViewSet, HomePageAPIView, BookViewSet, SearchListAPIView

router = DefaultRouter()
router.register('book-list', BookViewSet, basename='لیست کتاب ها')

urlpatterns = [
                  path('home/', HomePageAPIView.as_view(), name='صفحه اصلی سامانه'),
                  path('search/', SearchListAPIView.as_view(), name='صفحه جست و جو سامانه'),
                  path('category/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),

              ] + router.urls
