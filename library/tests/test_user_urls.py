from model_bakery import baker
from rest_framework import status
import pytest
from rest_framework.status import HTTP_401_UNAUTHORIZED

from library.models import ReviewRequest, Book, BorrowRequest


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


@pytest.fixture
def user_get_books(api_client):
    def get_books():
        return api_client.get('/user/books/')

    return get_books


@pytest.fixture
def user_get_single_book(api_client):
    def get_single_book(book_id):
        return api_client.get(f'/user/books/{book_id}/')

    return get_single_book


@pytest.fixture
def user_post_borrow_request(api_client):
    def user_post_borrow(book_id, data):
        return api_client.post(f'/user/books/{book_id}/borrow/', data)

    return user_post_borrow


@pytest.fixture
def user_get_requests(api_client):
    def get_requests():
        return api_client.get('/user/requests/')

    return get_requests


@pytest.fixture
def user_post_extension_request(api_client):
    def user_post_extension(book_id, data):
        return api_client.post(f'/user/books/{book_id}/extension/', data)

    return user_post_extension


@pytest.fixture
def user_post_return_request(api_client):
    def user_post_return(book_id, data):
        return api_client.post(f'/user/books/{book_id}/return/', data=data)

    return user_post_return


@pytest.fixture
def user_get_single_books_reviews(api_client):
    def get_single_book_reviews(book_id):
        return api_client.get(f'/user/books/{book_id}/reviews/')

    return get_single_book_reviews


@pytest.fixture
def user_post_available_reminder_book_request(api_client):
    def post_available_reminder_request(book_id, data):
        return api_client.post(f'/user/books/{book_id}/available/', data=data)

    return post_available_reminder_request


@pytest.fixture
def user_get_my_books(api_client):
    def get_user_books():
        return api_client.get('/user/my-books/')

    return get_user_books


@pytest.fixture
def user_get_notifications(api_client):
    def get_user_notifications():
        return api_client.get('/user/notifications/')

    return get_user_notifications


@pytest.fixture
def super_user_get_requests(api_client):
    def get_requests():
        return api_client.get('/super-user/requests/')

    return get_requests


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


@pytest.mark.django_db
class TestGetUserBooks:
    def test_if_user_is_annonymous_returns_401(self, user_get_books):
        response = user_get_books()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_200(self, api_client, user, user_get_books):
        api_client.force_authenticate(user=user)

        response = user_get_books()

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestGetSingleBook:
    def test_if_user_is_annonymous_returns_401(self, user_get_single_book):
        response = user_get_single_book(book_id=1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_200(self, api_client, user, user_get_single_book):
        api_client.force_authenticate(user=user)
        book = baker.make(Book)
        response = user_get_single_book(book_id=book.id)

        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_authenticated_but_retrieve_none_existing_book_404(self, api_client, user, user_get_single_book):
        api_client.force_authenticate(user=user)
        response = user_get_single_book(book_id=9999)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestPostCreateUserBorrowRequest:
    def test_if_user_is_annonymous_returns_401(self, user_post_borrow_request):
        response = user_post_borrow_request(book_id=1, data={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_create_borrow_returns_201(self, api_client, user, user_post_borrow_request):
        api_client.force_authenticate(user=user)
        book = baker.make(Book)
        data = {
            'user': user.id,
            'book': book.id,
            'type': 'borrow',
            'time': 14,
        }
        response = user_post_borrow_request(book_id=book.id, data=data)

        assert response.status_code == status.HTTP_201_CREATED

    def test_if_user_is_authenticate_but_data_is_invalid_returns_400(self, user, api_client, user_post_borrow_request):
        api_client.force_authenticate(user=user)

        book = baker.make(Book)
        data = {
            'user': user.id,
            'book': book.id,
            'type': 'borrow',
            'time': 15,
        }
        response = user_post_borrow_request(book_id=book.id, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestGetUserRequests:
    def test_if_user_is_annonymous_returns_401(self, user_get_requests):
        response = user_get_requests()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated(self, user, api_client, user_get_requests):
        api_client.force_authenticate(user=user)
        response = user_get_requests()

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestPostCreateUserExtensionRequest:
    def test_if_user_is_annonymous_returns_401(self, user_post_extension_request):
        response = user_post_extension_request(book_id=1, data={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_create_extension_returns_201(self, api_client, user, user_post_extension_request):
        api_client.force_authenticate(user=user)
        book = baker.make(Book)

        baker.make(BorrowRequest, user=user, book=book, time=3, status='accepted')

        data = {
            'user': user.id,
            'book': book.id,
            'type': 'extension',
            'time': 3,
        }
        response = user_post_extension_request(book_id=book.id, data=data)

        assert response.status_code == status.HTTP_201_CREATED

    def test_if_user_is_authenticate_but_data_is_invalid_returns_400(self, user, api_client,
                                                                     user_post_extension_request):
        api_client.force_authenticate(user=user)
        book = baker.make(Book)

        baker.make(BorrowRequest, user=user, book=book, time=14, status='accepted')

        data = {
            'user': user.id,
            'book': book.id,
            'type': 'extension',
            'time': 100,
        }
        response = user_post_extension_request(book_id=book.id, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestPostCreateUserReturnRequest:
    def test_if_user_is_annonymous_returns_401(self, user_post_return_request):
        response = user_post_return_request(book_id=1, data={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_201(self, user, api_client, user_post_return_request):
        api_client.force_authenticate(user=user)
        book = baker.make(Book)
        baker.make(BorrowRequest, user=user, book=book, time=14, status='accepted')

        post_data = {
            'book': book.id,
            'user': user.id,
            'score': 5,
            'description': 'test'
        }

        response = user_post_return_request(book_id=book.id, data=post_data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_if_suer_is_authenticated_but_data_is_invalid_returns_400(self, user, api_client, user_post_return_request):
        api_client.force_authenticate(user=user)
        book = baker.make(Book)
        baker.make(BorrowRequest, user=user, book=book, time=14, status='accepted')

        post_data = {
            'book': book.id,
            'user': user.id,
            'score': 8,
            'description': 'test'
        }

        response = user_post_return_request(book_id=book.id, data=post_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestGetUserSingleBookReviews:
    def test_if_user_is_annonymous_returtns_401(self, user_get_single_books_reviews):
        response = user_get_single_books_reviews(book_id=1)

        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_200(self, user, api_client, user_get_single_books_reviews):
        api_client.force_authenticate(user=user)
        book = baker.make(Book)
        response = user_get_single_books_reviews(book_id=book.id)

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestUserPostAvailableReminderBookRequest:
    def test_if_user_is_annonymous_returns_401(self, user_post_available_reminder_book_request):
        response = user_post_available_reminder_book_request(book_id=99, data={})

        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_200(self, user, api_client, user_post_available_reminder_book_request):
        api_client.force_authenticate(user=user)
        book = baker.make(Book, count=0)
        response = user_post_available_reminder_book_request(book_id=book.id, data={})

        assert response.status_code == status.HTTP_201_CREATED

    def test_if_user_is_authenticated_but_post_invalid_data_400(self, user, api_client,
                                                                user_post_available_reminder_book_request):
        api_client.force_authenticate(user=user)
        response = user_post_available_reminder_book_request(book_id=600, data={})

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestGetUserMyBooks:
    def test_if_user_is_annonymous_returns_401(self, user_get_my_books):
        response = user_get_my_books()

        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_200(self, user, api_client, user_get_my_books):
        api_client.force_authenticate(user=user)
        response = user_get_my_books()

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestGetUserNotifications:
    def test_if_user_is_annonymous_returns_401(self, user_get_notifications):
        response = user_get_notifications()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authentiacted_returns_200(self, user, api_client, user_get_notifications):
        api_client.force_authenticate(user=user)
        response = user_get_notifications()

        assert response.status_code == status.HTTP_200_OK


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
