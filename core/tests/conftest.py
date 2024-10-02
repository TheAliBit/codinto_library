from model_bakery import baker
from rest_framework.test import APIClient
import pytest
from core.utils import create_test_image
from core.models import Profile


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return Profile.objects.create_user(username="testuser", password="testpassword", email="test@test.com")


@pytest.fixture
def staff_user():
    return Profile.objects.create_user(username="staffuser", password="testpassword", email="test@test.com",
                                       is_staff=True)


@pytest.fixture
def super_user_list_create_url():
    return '/super-user/users/'
