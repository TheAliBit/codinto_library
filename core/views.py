from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import authenticate
from .utils import black_list_refresh_token, get_access_from_refresh
from core.serializers.registration_serializers import LoginSerializer, RefreshSerializer
from core.serializers.profile_serializers import ProfileSerializer
from rest_framework import status, mixins, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate


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


# class ProfileAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         user = request.user
#         serializer = ProfileSerializer(user)
#         default_content = serializer.data
#         default_content['password'] = ''
#         return Response({
#             "Hint": ".دیکشنری زیر را کپی و در قسمت پست بزارید و موارد را تغییر دهید",
#             "current_profile": default_content
#         })
#
#     def put(self, request):
#         password = request.data.get('password')
#         if not password:
#             return Response({"message": "!پسورد را وارد کنید"}, status=status.HTTP_400_BAD_REQUEST)
#
#         user = authenticate(username=request.user.username, password=password)
#         if user is None:
#             return Response({"message": "!پسورد اشتباه است"}, status=status.HTTP_400_BAD_REQUEST)
#
#         user = request.user
#         serializer = ProfileSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileUpdateView(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        generics.GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        password = request.data.get('password')
        if not password:
            return Response({"error": "!رمزعبور را وارد کنید"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=request.user.username, password=password)
        if user is None:
            return Response({"error": "!رمزعبور اشتباه است"}, status=status.HTTP_400_BAD_REQUEST)

        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        # Exclude username and password from the update
        data = {k: v for k, v in serializer.validated_data.items() if k not in ['user', 'password']}
        serializer.save(**data)
