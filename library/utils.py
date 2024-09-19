from datetime import timedelta

from django.utils import timezone

from django.shortcuts import get_object_or_404

from codinto_library.utils import send_sms
from .models import BorrowRequest, ExtensionRequest, Book, ReturnRequest, Notification


def calculate_end_date(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user = request.user

    try:
        borrow_request = BorrowRequest.objects.get(user=user, book=book, status='accepted')
        if ReturnRequest.objects.filter(user=user, book=book, status='accepted').exists():
            return {"message": "! شما مطالعه ای کتاب را به پایان رسانده اید"}
        try:
            extension_request = ExtensionRequest.objects.get(user=user, book=book, status='accepted')
            extension_duration = extension_request.duration
            end_date = borrow_request.end_date + timedelta(days=extension_duration)
            now = timezone.now()
            remaining = end_date - now
            return remaining.days
        except ExtensionRequest.DoesNotExist:
            now = timezone.now()
            end_date = borrow_request.end_date
            remaining = end_date - now
            return remaining.days
    except BorrowRequest.DoesNotExist:
        return {"message": "!این کتاب را تا به حال به امانت نبرده اید"}


def handle_availability(book_id):
    book = get_object_or_404(Book, id=book_id)

    available_notifications = Notification.objects.filter(book=book, type='available')
    for notification in available_notifications:
        user_profile = notification.user
        if user_profile and user_profile.phone_number:
            message = f"سلام {user_profile} عزیز, کتاب {book.title} موجود شد"
            send_sms(user_profile.phone_number, message)
            available_notifications.delete()
