from http.client import responses

from django.utils.encoding import force_str
from model_bakery import baker
from urllib3 import request

from core.models import Profile
from core.utils import create_test_image
from rest_framework import status
import pytest

from library.models import ReviewRequest, Book


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


@pytest.fixture
def user_get_single_reviews(api_client):
    def get_single_reviews(review_id):
        return api_client.get(f'/user/reviews/{review_id}/')

    return get_single_reviews


@pytest.fixture
def user_delete_single_reviews(api_client):
    def delete_single_reviews(review_id):
        return api_client.delete(f'/user/reviews/{review_id}/')

    return delete_single_reviews


@pytest.fixture
def user_update_single_reviews(api_client):
    def update_single_reviews(review_id, data):
        return api_client.put(f'/user/reviews/{review_id}/', data=data)

    return update_single_reviews


@pytest.mark.django_db
class TestGetUserHomePage:
    def test_if_user_is_annonymous_returns_401(self, user_get_home_page):
        response = user_get_home_page()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_200(self, api_client, user, user_get_home_page):
        api_client.force_authenticate(user=user)

        response = user_get_home_page()

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestGetUserSearchPage:
    def test_if_user_is_annonymous_returns_401(self, user_get_search_page):
        response = user_get_search_page()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_200(self, api_client, user, user_get_search_page):
        api_client.force_authenticate(user=user)

        response = user_get_search_page()

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestGetUserReviews:
    def test_if_user_is_annonymous_returns_401(self, user_get_reviews):
        response = user_get_reviews()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_200(self, api_client, user, user_get_reviews):
        api_client.force_authenticate(user=user)

        response = user_get_reviews()

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestUserGetSingleReviews:
    def test_if_user_is_annonymous_returns_401(self, user_get_single_reviews):
        response = user_get_single_reviews(review_id=1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_200(self, api_client, user, user_get_single_reviews):
        api_client.force_authenticate(user=user)

        review = baker.make(ReviewRequest, user=user)

        response = user_get_single_reviews(review_id=review.id)

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestUserDeleteSingleReviews:
    def test_if_user_is_annonymous_returns_401(self, user_delete_single_reviews):
        response = user_delete_single_reviews(review_id=1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_deletes_none_existing_review(self, api_client, user, user_delete_single_reviews):
        api_client.force_authenticate(user=user)
        response = user_delete_single_reviews(review_id=9999)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_deletes_single_review_returns_204(self, user, api_client, user_delete_single_reviews):
        api_client.force_authenticate(user=user)
        review = baker.make(ReviewRequest, user=user)
        response = user_delete_single_reviews(review_id=review.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestUpdateSingleReviews:
    def test_if_user_is_not_authenticated_updates_returns_401(self, user_update_single_reviews):
        response = user_update_single_reviews(review_id=1, data={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_updates_returns_200(self, user, api_client, user_update_single_reviews):
        api_client.force_authenticate(user=user)
        review = baker.make(ReviewRequest, user=user)

        updated_data = {
            'score': 2,
            'description': 'test'
        }

        response = user_update_single_reviews(review_id=review.id, data=updated_data)

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_updates_invalid_data_returns_400(self, user, api_client, user_update_single_reviews):
        api_client.force_authenticate(user=user)
        review = baker.make(ReviewRequest, user=user)
        updated_data = {
            'score': 8,
            'description': ''
        }
        response = user_update_single_reviews(review_id=review.id, data=updated_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
