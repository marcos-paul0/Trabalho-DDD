"""
Celery configuration for media_vault project.
"""

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "media_vault.settings")

app = Celery("media_vault")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
