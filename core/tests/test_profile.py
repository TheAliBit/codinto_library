from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker
from rest_framework import status
import pytest
from core.models import Profile


@pytest.mark.django_db
class TestCreateProfile:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.post('/super-user/users/', {'title': 'a'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client):
        api_client.force_authenticate(user={})
        response = api_client.post('/super-user/users/', {'title': 'a'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, api_client):
        api_client.force_authenticate(user=User(is_staff=True))
        response = api_client.post('/super-user/users/', {'username': ''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['username'] is not None

    def test_if_data_is_valid_returns_201(self, api_client):
        api_client.force_authenticate(user=User(is_staff=True))

        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b',
            content_type='image/jpeg'
        )
        context = {
            'username': 'a',
            'password': 'password123',
            'first_name': 'First',
            'last_name': 'Last',
            'phone_number': '09123430252',
            'email': 'user@example.com',
            'telegram_id': '123456',
            'picture': image
        }
        response = api_client.post('/super-user/users/', context)
        print(response.data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
