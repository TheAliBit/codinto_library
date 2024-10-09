from rest_framework.test import APIClient
import pytest
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


