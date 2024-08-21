from django.urls import path
from rest_framework.routers import DefaultRouter

from core.views import LoginAPIView, LogoutAPIView, RefreshAPIView, ProfileUpdateView
from library.views import BookView

router = DefaultRouter()

urlpatterns = [
                  path('login/', LoginAPIView.as_view(), name='ورود'),
                  path('logout/', LogoutAPIView.as_view(), name='خروج'),
                  path('refresh/', RefreshAPIView.as_view(), name='رفرش'),
                  path('profile/', ProfileUpdateView.as_view(), name='پروفایل'),

              ] + router.urls
