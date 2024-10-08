from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from .permissions import IsNotSelf
from .utils import black_list_refresh_token, get_access_from_refresh
from core.serializers.registration_serializers import LoginSerializer, RefreshSerializer
from core.serializers.profile_serializers import ProfileSerializer, AdminSingleProfileSerializer
from rest_framework import status, mixins, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from core.models import Profile


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
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access = get_access_from_refresh(serializer.data['refresh'])
        return Response(data={'access': access}, status=status.HTTP_200_OK)


class ProfileUpdateView(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        generics.GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    queryset = Profile.objects.all()

    def get_object(self):
        # Return the user object itself
        return self.request.user

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        new_username = request.data.get('username')
        currernt_username = self.request.user.username

        # new_phone_number = request.data.get('phone_number')
        # current_phone_number = self.request.user.phone_number
        if new_username and new_username != currernt_username:
            if Profile.objects.filter(username=new_username).exists():
                raise ValidationError({'error': "!نام کاربری باید یکتا باشد"})

        # if new_phone_number and new_phone_number != current_phone_number:
        #     if Profile.objects.filter(phone_number=new_phone_number).exists():
        #         raise ValidationError("!کاربری با این شماره تلفن وجود دارد")

        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()


class SearchUserView(ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'telegram_id']
    queryset = Profile.objects.all()


class AdminListProfileView(ListAPIView, CreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'telegram_id']

    def get_queryset(self):
        return Profile.objects.all().exclude(id=self.request.user.id, is_superuser=True)


class AdminSingleProfileView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    serializer_class = AdminSingleProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, IsNotSelf]

    def get_queryset(self):
        return Profile.objects.all()
