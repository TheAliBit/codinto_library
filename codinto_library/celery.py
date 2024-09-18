import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codinto_library.settings')

celery = Celery('codinto_library')

celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()