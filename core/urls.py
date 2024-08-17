from django.urls import path
from core.views import LoginAPIView, LogoutAPIView, RefreshAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='ورود'),
    path('logout/', LogoutAPIView.as_view(), name='خروج'),
    path('refresh/', RefreshAPIView.as_view(), name='رفرش'),
]
