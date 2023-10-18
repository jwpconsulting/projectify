"""Test settings."""
from os import (
    environ,
)

# flake8: noqa: F401, F403
from .base import *


class Test(Base):
    """Test configuration."""

    # TODO populate me
    SECRET_KEY = "test"

    FRONTEND_URL = "https://example.com"

    # Email
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    EMAIL_EAGER = True

    # GraphQL
    GRAPHIQL_ENABLE = False  #

    # Stripe
    STRIPE_SECRET_KEY = "null"
    STRIPE_ENDPOINT_SECRET = "null"

    # Copy static files storage from production settings to test
    # collectstatic
    if "TEST_STATICFILES_STORAGE" in environ:
        STORAGES = Base.STORAGES
        STORAGES["staticfiles"][
            "BACKEND"
        ] = "whitenoise.storage.CompressedManifestStaticFilesStorage"

    # Celery
    CELERY_BROKER_URL = "memory://"
