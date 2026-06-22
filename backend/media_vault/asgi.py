"""
Production ASGI config for media_vault project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "media_vault.settings")

application = get_asgi_application()
