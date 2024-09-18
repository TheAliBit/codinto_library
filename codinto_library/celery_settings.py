CELERY_BROKER_URL = 'redis://localhost:6379/1'
CELERY_BEAT_SCHEDULE = {
    'notify_customer': {
        'task': 'library.tasks.notify_customer',
        'schedule': 10.0,  # Every 10 seconds
        'args': ['hello world'],
    },
}
