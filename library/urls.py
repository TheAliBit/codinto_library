from django.urls import path
from rest_framework.routers import DefaultRouter

from library.views import CategoryViewSet, MainPageAPIView

router = DefaultRouter()

urlpatterns = [
                  path('category/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
                  path('main-page/', MainPageAPIView.as_view(), name='newest-books'),
              ] + router.urls
