# flake8: noqa: F401, F403
import os

from .base import *


class Development(Base):
    """Development configuration."""

    SECRET_KEY = "development"

    # Debug
    DEBUG = True
    DEBUG_TOOLBAR = True
    INTERNAL_IPS = ("127.0.0.1",)

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
    STORAGES = Base.STORAGES
    STORAGES["default"]["BACKEND"] = "projectify.storage.LocalhostStorage"

    # Stripe
    STRIPE_PUBLISHABLE_KEY = os.environ["STRIPE_PUBLISHABLE_KEY"]
    STRIPE_SECRET_KEY = os.environ["STRIPE_SECRET_KEY"]
    STRIPE_PRICE_OBJECT = os.environ["STRIPE_PRICE_OBJECT"]
    STRIPE_ENDPOINT_SECRET = os.environ["STRIPE_ENDPOINT_SECRET"]

    # Safari workaround for sessionid cookie
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = "Lax"
