from django.urls import path
from .views import say_ok

urlpatterns = [
    path('ok/', say_ok)
]
