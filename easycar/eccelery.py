from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
app = Celery()

app.config_from_object(settings)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, force=True)
