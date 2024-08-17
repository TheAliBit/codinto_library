from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import authenticate
from .utils import black_list_refresh_token, get_access_from_refresh
from core.serializers.registration_serializers import LoginSerializer, RefreshSerializer


# Create your views here.
class LoginAPIView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(username=serializer.validated_data['username'],
                            password=serializer.validated_data['password'])
        if not user:
            return Response({'error': 'نام کاربری یا رمز عبور اشتباه است!'}, status=status.HTTP_400_BAD_REQUEST)

        access = str(AccessToken.for_user(user))
        refresh = str(RefreshToken.for_user(user))
        return Response(data={'access': access, 'refresh': refresh}, status=status.HTTP_200_OK)


class LogoutAPIView(generics.CreateAPIView):
    serializer_class = RefreshSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        black_list_refresh_token(serializer.data['refresh'])
        return Response(data={'message': 'با موفقیت خارج شدید!'}, status=status.HTTP_200_OK)


class RefreshAPIView(generics.CreateAPIView):
    serializer_class = RefreshSerializer
    permission_classes = [AllowAny]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access = get_access_from_refresh(serializer.data['refresh'])
        return Response(data={'access': access}, status=status.HTTP_200_OK)
