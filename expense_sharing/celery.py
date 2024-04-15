from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_sharing.settings')

app = Celery('expense_sharing')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Define a Celery beat schedule for the weekly task
app.conf.beat_schedule = {
    'update_user_data_weekly': {
        'task': 'core.tasks.update_user_data_on_s3',
        'schedule': crontab(hour=0, minute=0, day_of_week=0),  # Run weekly on Sunday at midnight
    },
}
