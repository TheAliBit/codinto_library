from django.urls import path
from rest_framework.routers import DefaultRouter
from core.views import LoginAPIView, LogoutAPIView, RefreshAPIView, ProfileUpdateView, SearchUserView, \
    AdminListProfileView, AdminSingleProfileView

router = DefaultRouter()

urlpatterns = [
                  path('login/', LoginAPIView.as_view(), name='ورود'),
                  path('logout/', LogoutAPIView.as_view(), name='خروج'),
                  path('refresh/', RefreshAPIView.as_view(), name='رفرش'),
                  path('profile/', ProfileUpdateView.as_view(), name='پروفایل'),
                  path('super-user/search-user/', SearchUserView.as_view(), name='search-user'),
                  path('super-user/users/', AdminListProfileView.as_view(), name='list-profile'),
                  path('super-user/users/<int:pk>/', AdminSingleProfileView.as_view(), name='single-profile'),

              ] + router.urls
