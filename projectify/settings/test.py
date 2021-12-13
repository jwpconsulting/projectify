# flake8: noqa: F401, F403
from .base import *


SECRET_KEY = "test"

STATIC_ROOT = None

FRONTEND_URL = "https://example.com"

CELERY_TASK_ALWAYS_EAGER = True

# Email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
