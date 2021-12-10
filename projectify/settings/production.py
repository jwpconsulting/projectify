"""Production settings."""
import os

# flake8: noqa: F401, F403
from .base import *


SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")

# Want forever-cacheable files and compression support? Just add this to your settings.py:
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

FRONTEND_URL = os.environ["FRONTEND_URL"]
