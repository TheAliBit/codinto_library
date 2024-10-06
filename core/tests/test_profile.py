from model_bakery import baker
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import Profile
from core.utils import create_test_image
from rest_framework import status
import pytest


# from library.tests.conftest import api_client


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


@pytest.fixture
def super_user_update_single_user(api_client):
    def update_user(user_id, data):
        return api_client.put(f'/super-user/users/{user_id}/', data=data)

    return update_user


@pytest.fixture
def user_update_its_profile(api_client):
    def update_user(data):
        return api_client.put('/user/profile/', data=data)

    return update_user


@pytest.fixture
def user_post_login(api_client):
    def post_login(data):
        return api_client.post('/user/login/', data=data)

    return post_login


@pytest.fixture
def user_post_refresh(api_client):
    def post_refresh(data):
        return api_client.post('/user/refresh/', data=data)

    return post_refresh


@pytest.fixture
def user_post_logout(api_client):
    def post_logout(data):
        return api_client.post('/user/logout/', data=data)

    return post_logout


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

    def test_if_user_is_admin_deletes_profile_returns_204(self, api_client, staff_user, super_user_delete_single_user):
        api_client.force_authenticate(user=staff_user)
        user = baker.make(Profile)
        response = super_user_delete_single_user(user_id=user.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert Profile.objects.filter(id=user.id).exists() is False

    def test_if_user_does_not_exist_returns_404(self, api_client, staff_user, super_user_delete_single_user):
        api_client.force_authenticate(user=staff_user)
        response = super_user_delete_single_user(user_id=999)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateUser:
    def test_if_user_is_anonymous_returns_401(self, super_user_update_single_user):
        response = super_user_update_single_user(user_id=1, data={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, user, super_user_update_single_user):
        api_client.force_authenticate(user=user)

        response = super_user_update_single_user(user_id=1, data={})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_update_and_returns_200(self, api_client, staff_user, super_user_update_single_user):
        api_client.force_authenticate(user=staff_user)

        user = baker.make(Profile)

        updated_data = {
            'username': 'test',
            'password': 'testpassword',
            'first_name': 'jamshit',
            'last_name': 'jamshiti',
            'email': 'test@gmail.com',
            'telegram_id': 'test_id',
            'phone_number': '09390605460',
        }

        response = super_user_update_single_user(user_id=user.id, data=updated_data)
        print(response.data)
        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_admin_but_data_is_bad_returns_400(self, api_client, staff_user, super_user_update_single_user):
        api_client.force_authenticate(user=staff_user)
        user = baker.make(Profile)

        updated_data = {
            'username': user.id,
            'password': 'testpassword',
            'first_name': 'jamshit',
            'last_name': 'jamshiti',
            'email': '',
            'telegram_id': '',
            'phone_number': '',
        }

        response = super_user_update_single_user(user_id=user.id, data=updated_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_does_not_exists_returns404(self, staff_user, api_client, super_user_update_single_user):
        api_client.force_authenticate(user=staff_user)
        response = super_user_update_single_user(user_id=999, data={})
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUserUpdateItsProfile:
    def test_if_user_is_annonymous_retruns_401(self, user_update_its_profile):
        response = user_update_its_profile(data={})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_updates_its_profile_returns_200(self, api_client, user, user_update_its_profile):
        api_client.force_authenticate(user=user)
        user = baker.make(Profile)
        image = create_test_image()
        updated_data = {
            'username': user.id,
            'password': 'testpassword',
            'first_name': 'jamshit',
            'last_name': 'jamshiti',
            'email': 'test@gmail.com',
            'telegram_id': 'test_id',
            'phone_number': '09390605460',
            'picture': image
        }
        response = user_update_its_profile(data=updated_data)

        assert response.status_code == status.HTTP_200_OK

    def test_if_data_is_not_valid_returns_400(self, user, api_client, user_update_its_profile):
        api_client.force_authenticate(user)
        user = baker.make(Profile)

        updated_data = {
            'username': user.id,
            'password': '',
            'first_name': 'jamshit',
            'last_name': 'jamshiti',
        }

        response = user_update_its_profile(data=updated_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestPostUserLogin:
    def test_if_user_returns_200(self, user_post_login):
        profile = Profile.objects.create(
            username='test',
            first_name='jamshit',
            last_name='jamshiti',
            email='test@gmail.com',
            telegram_id='test_id',
            phone_number='09390605460',
            picture=create_test_image()
        )

        profile.set_password('shift7833')
        profile.save()

        post_data = {
            'username': 'test',
            'password': 'shift7833',
        }

        response = user_post_login(data=post_data)

        assert response.status_code == status.HTTP_200_OK

    def test_if_not_user_returns_400(self, user_post_login):
        post_data = {
            'username': 'test',
            'password': 'shift7833',
        }

        response = user_post_login(data=post_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestPostRefresh:
    def test_if_user_is_annonymous_retruns_401(self, user_post_refresh):
        response = user_post_refresh(data={})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_but_token_is_invalid_reutrns_400(self, user_post_refresh, api_client, user):
        api_client.force_authenticate(user=user)
        response = user_post_refresh(data={})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_and_token_returns_200(self, user_post_refresh, api_client, user):
        api_client.force_authenticate(user=user)

        profile = Profile.objects.create(
            username='test',
            first_name='jamshit',
            last_name='jamshiti',
            email='test@gmail.com',
            telegram_id='test_id',
            phone_number='09390605460',
            picture=create_test_image()
        )

        profile.set_password('shift7833')
        profile.save()

        refresh_token = RefreshToken.for_user(profile)

        refresh_token = {
            'refresh': str(refresh_token)
        }

        response = user_post_refresh(data=refresh_token)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestUserLogout:
    def test_if_user_is_annonymous_returns_401(self, user_post_logout):
        response = user_post_logout(data={})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_but_token_is_invalid_reutrns_400(self, user_post_logout, api_client, user):
        api_client.force_authenticate(user=user)
        response = user_post_logout(data={})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_user_and_token_returns_200(self, user_post_logout, api_client, user):
        api_client.force_authenticate(user=user)

        profile = Profile.objects.create(
            username='test',
            first_name='jamshit',
            last_name='jamshiti',
            email='test@gmail.com',
            telegram_id='test_id',
            phone_number='09390605460',
            picture=create_test_image()
        )

        profile.set_password('shift7833')
        profile.save()

        refresh_token = RefreshToken.for_user(profile)

        logout_data = {
            'refresh': str(refresh_token)
        }

        response = user_post_logout(data=logout_data)

        assert response.status_code == status.HTTP_200_OK
