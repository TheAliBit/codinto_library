from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()


def get_jwt_tokens(user):
    access = AccessToken.for_user(user)
    refresh = RefreshToken.for_user(user)
    return (access, refresh)


def black_list_refresh_token(refresh):
    refresh_token = RefreshToken(refresh)
    refresh_token.blacklist()


def get_access_from_refresh(refresh):
    refresh = RefreshToken(refresh)
    access = str(refresh.access_token)
    return access


def create_test_image():
    image = SimpleUploadedFile(name='test_image.jpg',
                               content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b',
                               content_type='image/jpeg')
    return image