from http.client import responses

from model_bakery import baker

from core.models import Profile
from core.utils import create_test_image
from rest_framework import status
import pytest


@pytest.fixture
def user_get_home_page(api_client):
    def get_home_page():
        return api_client.get('/user/home/')

    return get_home_page


@pytest.fixture
def user_get_search_page(api_client):
    def get_search_page():
        return api_client.get('/user/search/')

    return get_search_page


@pytest.fixture
def user_get_reviews(api_client):
    def get_reviews():
        return api_client.get('/user/reviews/')

    return get_reviews


@pytest.mark.django_db
class TestUserHomePage:
    def test_if_user_is_annonymous_returns_401(self, user_get_home_page):
        response = user_get_home_page()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_200(self, api_client, user, user_get_home_page):
        api_client.force_authenticate(user=user)

        response = user_get_home_page()

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestUserSearchPage:
    def test_if_user_is_annonymous_returns_401(self, user_get_search_page):
        response = user_get_search_page()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_200(self, api_client, user, user_get_search_page):
        api_client.force_authenticate(user=user)

        response = user_get_search_page()

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestUserReviews:
    def test_if_user_is_annonymous_returns_401(self, user_get_reviews):
        response = user_get_reviews()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_200(self, api_client, user, user_get_reviews):
        api_client.force_authenticate(user=user)

        response = user_get_reviews()

        assert response.status_code == status.HTTP_200_OK
