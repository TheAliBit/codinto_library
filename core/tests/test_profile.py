from model_bakery import baker

from core.models import Profile
from core.utils import create_test_image
from rest_framework import status
import pytest


@pytest.fixture
def super_user_create(api_client):
    def create_user(data):
        return api_client.post('/super-user/users/', data=data)

    return create_user


@pytest.fixture
def super_user_get(api_client):
    def get_user():
        return api_client.get('/super-user/users/')

    return get_user


@pytest.fixture
def super_user_search(api_client):
    def get_user():
        return api_client.get('/super-user/search-users/')

    return get_user


@pytest.fixture
def super_user_get_single_user(api_client):
    def get_user(user_id):
        return api_client.get(f'/super-user/users/{user_id}/')

    return get_user


@pytest.fixture
def super_user_delete_single_user(api_client):
    def delete_user(user_id):
        return api_client.delete(f'/super-user/users/{user_id}/')

    return delete_user


@pytest.mark.django_db
class TestCreateProfile:
    def test_if_user_is_anonymous_returns_401(self, api_client, super_user_create):
        response = super_user_create(data={})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, user, super_user_create):
        api_client.force_authenticate(user=user)
        response = super_user_create({'title': 'a'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, api_client, staff_user, super_user_create):
        api_client.force_authenticate(user=staff_user)
        response = super_user_create({'username': ''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_201(self, api_client, staff_user, super_user_create):
        api_client.force_authenticate(user=staff_user)
        image = create_test_image()
        context = {
            'username': 'test',
            'password': 'testpassword',
            'first_name': 'jamshit',
            'last_name': 'jamshiti',
            'email': 'test@gmail.com',
            'telegram_id': 'test_id',
            'phone_number': '09390605460',
            'picture': image,
        }
        response = super_user_create(context)
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestGetProfile:
    def test_if_user_is_anonymous_returns_401(self, super_user_get):
        response = super_user_get()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, super_user_get, api_client, user):
        api_client.force_authenticate(user=user)

        response = super_user_get()

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_200(self, super_user_get, api_client, staff_user):
        api_client.force_authenticate(user=staff_user)

        response = super_user_get()

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestGetInSuperUserSearch:
    def test_if_user_is_anonymous_returns_401(self, super_user_search):
        response = super_user_search()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, user, super_user_search):
        api_client.force_authenticate(user=user)

        response = super_user_search()

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_200(self, api_client, super_user_search, staff_user):
        api_client.force_authenticate(user=staff_user)
        response = super_user_search()
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestRetrieveUserDetail:
    def test_if_user_is_anonymous_returns_401(self, super_user_get_single_user):
        response = super_user_get_single_user(user_id=1)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, user, super_user_get_single_user):
        api_client.force_authenticate(user=user)
        response = super_user_get_single_user(user_id=1)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_200(self, api_client, staff_user, super_user_get_single_user):
        api_client.force_authenticate(user=staff_user)
        user = baker.make(Profile)
        response = super_user_get_single_user(user_id=user.id)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == user.id


@pytest.mark.django_db
class TestDeleteUser:
    def test_if_user_is_anonymous_returns_401(self, super_user_delete_single_user):
        response = super_user_delete_single_user(user_id=1)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, user, super_user_delete_single_user):
        api_client.force_authenticate(user=user)
        response = super_user_delete_single_user(user_id=1)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_deletes_profile_returns_200(self, api_client, staff_user, super_user_delete_single_user):
        api_client.force_authenticate(user=staff_user)
        user = baker.make(Profile)
        response = super_user_delete_single_user(user_id=user.id)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Profile.objects.filter(id=user.id).exists() is False
