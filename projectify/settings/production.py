"""Production settings."""
import os

# flake8: noqa: F401, F403
from .base import *


SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")

# Want forever-cacheable files and compression support? Just add this to your settings.py:
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

FRONTEND_URL = os.environ["FRONTEND_URL"]

ANYMAIL = {
    "MAILGUN_API_KEY": os.environ["MAILGUN_API_KEY"],
    "MAILGUN_SENDER_DOMAIN": os.environ["MAILGUN_DOMAIN"],
}
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
