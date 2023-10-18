"""Test settings."""
from .base import (
    Base,
)


class Test(Base):
    """Test configuration."""

    # TODO populate me
    SECRET_KEY = "test"

    FRONTEND_URL = "https://example.com"

    # Email
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    EMAIL_EAGER = True

    # GraphQL
    GRAPHIQL_ENABLE = False

    # Stripe
    # TODO
    # Something other than null would be great, like Optional[str]
    STRIPE_SECRET_KEY = "null"
    STRIPE_ENDPOINT_SECRET = "null"

    # Celery
    CELERY_BROKER_URL = "memory://"


class TestCollectstatic(Test):
    """Settings to test static file collection needed for whitenoise."""

    STORAGES = {
        **Base.STORAGES,
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
