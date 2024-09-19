
from celery import shared_task

from codinto_library.utils import send_sms


@shared_task
def send_sms_task(phone_number, message):
    send_sms(phone_number, message)