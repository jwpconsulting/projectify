# flake8: noqa: F401, F403
from .base import *


SECRET_KEY = "development"

DEBUG = True

CORS_ALLOWED_ORIGINS = ("http://localhost:3000",)

FRONTEND_URL = "http://localhost:8000/"
