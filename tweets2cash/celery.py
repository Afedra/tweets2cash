# -*- coding: utf-8 -*-

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

from django.conf import settings

try:
    from settings import celery_local as celery_settings
except ImportError:
    from settings import celery as celery_settings

app = Celery('tweets2cash')
app.config_from_object(celery_settings)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
