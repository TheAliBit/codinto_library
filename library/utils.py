from django.shortcuts import get_object_or_404

from .models import BorrowRequest, ExtensionRequest, Book, ReturnRequest


def calculate_end_date(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user = request.user

    try:
        borrow_request = BorrowRequest.objects.get(user=user, book=book, status='accepted')
        borrow_duration = borrow_request.duration

        if ReturnRequest.objects.filter(user=user, book=book, status='accepted').exists():
            return {"message": "شما این کتاب را یکبار مطالعه کردید"}
        try:
            extension_request = ExtensionRequest.objects.get(user=user, book=book, status='accepted')
            extension_duration = extension_request.duration

            return borrow_duration + extension_duration
        except ExtensionRequest.DoesNotExist:
            return borrow_duration
    except BorrowRequest.DoesNotExist:
        return {"message": "! این کتاب را به امانت نبرده اید"}
