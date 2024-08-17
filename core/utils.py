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
