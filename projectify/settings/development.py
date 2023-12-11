"""Development settings."""
import logging
import os
from collections.abc import (
    Iterable,
    Sequence,
)
from typing import Optional

from dotenv import (
    load_dotenv,
)

from .base import (
    Base,
)

logger = logging.getLogger(__name__)


def add_debug_middleware(middleware: Sequence[str]) -> Iterable[str]:
    """Add the debug toolbar to debug middleware."""
    gzip_middleware = "django.middleware.gzip.GZipMiddleware"
    for m in middleware:
        if m == gzip_middleware:
            yield m
            yield "debug_toolbar.middleware.DebugToolbarMiddleware"
        else:
            yield m


def environ_get_or_warn(key: str) -> Optional[str]:
    """Get an environment variable or warn that it is not set."""
    value = os.environ.get(key)

    if value is not None:
        return value

    logger.warn(f"{key} needed for settings was not set in environment")
    return None


class Development(Base):
    """Development configuration."""

    SECRET_KEY = "development"

    INSTALLED_APPS = (
        *Base.INSTALLED_APPS,
        "debug_toolbar",
    )

    MIDDLEWARE = list(add_debug_middleware(Base.MIDDLEWARE))

    # Debug
    DEBUG = True
    DEBUG_TOOLBAR = True
    INTERNAL_IPS = ("127.0.0.1",)

    CORS_ALLOWED_ORIGINS = (
        # Vite dev
        "http://localhost:3000",
        # Storybook
        "http://localhost:6006",
    )
    CSRF_TRUSTED_ORIGINS = (
        # Vite dev
        "http://localhost:3000",
        # Storybook
        "http://localhost:6006",
    )

    FRONTEND_URL = "http://localhost:3000/"

    CELERY_TASK_ALWAYS_EAGER = True
    # TODO if celery is eager, a broker should not be necessary, right?
    CELERY_BROKER_URL = os.environ["REDIS_TLS_URL"]

    # Email
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    # Media
    SERVE_MEDIA = True

    STORAGES = {
        **Base.STORAGES,
        "default": {
            "BACKEND": "projectify.storage.LocalhostStorage",
        },
    }

    # Stripe
    STRIPE_PUBLISHABLE_KEY = environ_get_or_warn("STRIPE_PUBLISHABLE_KEY")
    STRIPE_SECRET_KEY = environ_get_or_warn("STRIPE_SECRET_KEY")
    STRIPE_PRICE_OBJECT = environ_get_or_warn("STRIPE_PRICE_OBJECT")
    STRIPE_ENDPOINT_SECRET = environ_get_or_warn("STRIPE_ENDPOINT_SECRET")

    # Safari workaround for sessionid cookie
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = "Lax"

    @classmethod
    def pre_setup(cls) -> None:
        """Load environment variables from .env."""
        super().pre_setup()
        load_dotenv()
