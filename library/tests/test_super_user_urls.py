from model_bakery import baker
from rest_framework import status
import pytest

from core.models import Profile
from core.utils import create_test_image
from library.models import Book, BorrowRequest, Category


@pytest.fixture
def super_user_get_requests(api_client):
    def get_requests():
        return api_client.get('/super-user/requests/')

    return get_requests


@pytest.fixture
def super_user_get_single_request(api_client):
    def get_single_request(request_id):
        return api_client.get(f'/super-user/requests/{request_id}/')

    return get_single_request


@pytest.fixture
def super_user_update_single_request(api_client):
    def update_single_request(request_id, data):
        return api_client.put(f'/super-user/requests/{request_id}/', data=data)

    return update_single_request


@pytest.fixture
def super_user_get_books(api_client):
    def get_books():
        return api_client.get('/super-user/books/')

    return get_books


@pytest.fixture
def super_user_post_books(api_client):
    def post_books(data):
        return api_client.post('/super-user/books/', data)

    return post_books


@pytest.mark.django_db
class TestGetSuperUserRequests:
    def test_if_user_is_annonymous_returns_401(self, super_user_get_requests):
        response = super_user_get_requests()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, user, api_client, super_user_get_requests):
        api_client.force_authenticate(user=user)
        response = super_user_get_requests()

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_200(self, staff_user, api_client, super_user_get_requests):
        api_client.force_authenticate(user=staff_user)
        response = super_user_get_requests()

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestGetSuperUserSingleRequest:
    def test_if_user_is_annonymous_returns_401(self, super_user_get_single_request):
        response = super_user_get_single_request(request_id=1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, user, api_client, super_user_get_single_request):
        api_client.force_authenticate(user=user)
        response = super_user_get_single_request(request_id=1)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_200(self, staff_user, api_client, super_user_get_single_request):
        api_client.force_authenticate(user=staff_user)
        user = baker.make(Profile)
        book = baker.make(Book)
        request = baker.make(BorrowRequest, user=user, book=book, time=14, status='accepted')
        response = super_user_get_single_request(request_id=request.id)

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_admin_but_request_does_not_exists_returns_404(self, staff_user, api_client,
                                                                      super_user_get_single_request):
        api_client.force_authenticate(user=staff_user)
        response = super_user_get_single_request(request_id=1000)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateSuperUserRequest:
    def test_if_user_is_annonymous_returns_401(self, super_user_update_single_request):
        response = super_user_update_single_request(request_id=1, data={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, user, api_client, super_user_update_single_request):
        api_client.force_authenticate(user=user)
        response = super_user_update_single_request(request_id=1, data={})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_200(self, staff_user, api_client, super_user_update_single_request):
        api_client.force_authenticate(user=staff_user)
        book = baker.make(Book)
        user = baker.make(Profile)
        request = baker.make(BorrowRequest, user=user, book=book, time=14)

        updated_data = {
            'status': 'accepted'
        }

        response = super_user_update_single_request(request_id=request.id, data=updated_data)

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_admin_but_data_is_invalid_returns_400(self, staff_user, api_client,
                                                              super_user_update_single_request):
        api_client.force_authenticate(user=staff_user)
        book = baker.make(Book)
        user = baker.make(Profile)
        request = baker.make(BorrowRequest, user=user, book=book, time=14)

        updated_data = {
            'status': 'iosadhgjksa'
        }

        response = super_user_update_single_request(request_id=request.id, data=updated_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestGetSuperUserBooks:
    def test_if_user_is_annonymous_returns_401(self, super_user_get_books):
        response = super_user_get_books()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_not_admin_returns_403(self, user, api_client, super_user_get_books):
        api_client.force_authenticate(user=user)
        response = super_user_get_books()

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_200(self, staff_user, api_client, super_user_get_books):
        api_client.force_authenticate(user=staff_user)
        response = super_user_get_books()

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestPostSuperUserBooks:
    def test_if_user_is_annobymous_returns_401(self, super_user_post_books):
        response = super_user_post_books(data={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, user, api_client, super_user_post_books):
        api_client.force_authenticate(user=user)
        response = super_user_post_books(data={})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_201(self, staff_user, api_client, super_user_post_books):
        api_client.force_authenticate(user=staff_user)

        image = create_test_image()
        user = baker.make(Profile)
        category = baker.make(Category)

        post_data = {
            "title": "asdf",
            "image": image,
            "author": "ehbdf",
            "translator": "asdf",
            "publisher": "sdafg",
            "volume_number": 12,
            "publication_year": 1400,
            "page_count": 150,
            "owner": user.id,
            "description": "sadsda",
            "category_id": category.id,
            "count": 10
        }

        response = super_user_post_books(data=post_data)

        print(response.data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_if_user_is_admin_but_data_is_invalid_returns_400(self, staff_user, api_client, super_user_post_books):
        api_client.force_authenticate(user=staff_user)

        image = create_test_image()
        user = baker.make(Profile)
        category = baker.make(Category)

        post_data = {
            "title": "asdf",
            "image": image,
            "author": "ehbdf",
            "translator": "asdf",
            "publisher": "sdafg",
            "volume_number": 12,
            "publication_year": 1400,
            "page_count": 150,
            "owner": user.id,
            "description": "sadsda",
            "category_id": category.id,
            "count": 'asdf'
        }

        response = super_user_post_books(data=post_data)

        print(response.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
