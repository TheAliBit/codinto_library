from celery.schedules import crontab

CELERY_BROKER_URL = 'redis://localhost:6379/1'
CELERY_BEAT_SCHEDULE = {
    'check_legal_borrow_date': {
        'task': 'library.tasks.check_legal_borrow_date',
        'schedule':  crontab(hour=0, minute=0),  # This runs every day at midnight (00:00)
    }
}