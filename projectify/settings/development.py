# flake8: noqa: F401, F403
import os

from .base import *


SECRET_KEY = "development"

DEBUG = True

CORS_ALLOWED_ORIGINS = ("http://localhost:3000",)
CSRF_TRUSTED_ORIGINS = ("http://localhost:3000",)

FRONTEND_URL = "http://localhost:3000/"

CELERY_TASK_ALWAYS_EAGER = True
CELERY_BROKER_URL = os.environ["REDIS_TLS_URL"]

# Email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# GraphQL
GRAPHIQL_ENABLE = True

# Media
SERVE_MEDIA = True
DEFAULT_FILE_STORAGE = "projectify.storage.LocalhostStorage"
