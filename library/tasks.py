from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from codinto_library.utils import send_sms
from library.models import BorrowRequest


@shared_task
def send_sms_task(phone_number, message):
    send_sms(phone_number, message)


@shared_task
def check_legal_borrow_date():
    today = timezone.now()

    requests = BorrowRequest.objects.filter(status='accepted', end_date__gte=today - timedelta(days=3))

    for request in requests:
        days_left = (request.end_date - today).days
        user = request.user

        if days_left == 3:
            message = f"یادآور: 3 روز مهلت باقی مانده برای تحویل کتاب {request.book.title} دارید"
        elif days_left == 2:
            message = f"یادآور: 2 روز مهلت باقی مانده برای تحویل کتاب {request.book.title} دارید"
        elif days_left == 1:
            message = f"یادآور: 1 روز مهلت باقی مانده برای تحویل کتاب {request.book.title} دارید"
        elif days_left == 0:
            message = f"یادآور: امروز روز تحویل کتاب {request.book.title} است"
        elif days_left == -1:
            message = f"اخطار: 1 روز تاخیر برای تحویل کتاب {request.book.title}"
        elif days_left == -2:
            message = f"اخطار: 2 روز تاخیر برای تحویل کتاب {request.book.title}"
        elif days_left == -3:
            message = f"اخطار: 3 روز تاخیر برای تحویل کتاب {request.book.title}"
        else:
            continue

        send_sms_task.delay(user.phone_number, message)
