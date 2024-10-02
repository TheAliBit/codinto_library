from django.urls import path
from rest_framework.routers import DefaultRouter
from core.views import LoginAPIView, LogoutAPIView, RefreshAPIView, ProfileUpdateView, SearchUserView, \
    AdminListProfileView, AdminSingleProfileView

router = DefaultRouter()

urlpatterns = [
                  path('user/login/', LoginAPIView.as_view(), name='ورود'),
                  path('user/logout/', LogoutAPIView.as_view(), name='خروج'),
                  path('user/refresh/', RefreshAPIView.as_view(), name='رفرش'),
                  path('user/profile/', ProfileUpdateView.as_view(), name='پروفایل'),
                  path('super-user/search-users/', SearchUserView.as_view(), name='search-user'),
                  path('super-user/users/', AdminListProfileView.as_view(), name='super_user_list_create'),
                  path('super-user/users/<int:pk>/', AdminSingleProfileView.as_view(), name='single-profile'),

              ] + router.urls
