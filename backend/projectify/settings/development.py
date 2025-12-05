# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021-2024 JWP Consulting GK
"""Development settings."""

import os
import warnings
from collections.abc import Iterable, Sequence
from typing import Optional

try:
    from dotenv import load_dotenv
except ImportError as e:
    raise RuntimeError(
        "dotenv was not found. Please check if dev dependencies have been installed"
    ) from e

from .base import Base
from .spectacular import SpectacularSettings


def add_dev_middleware(middleware: Sequence[str]) -> Iterable[str]:
    """Add the debug toolbar to debug middleware."""
    gzip_middleware = "django.middleware.gzip.GZipMiddleware"
    for m in middleware:
        if m == gzip_middleware:
            yield m
            yield "debug_toolbar.middleware.DebugToolbarMiddleware"
            yield "projectify.middleware.microsloth"
            yield "projectify.middleware.errorsloth"
            yield "django_browser_reload.middleware.BrowserReloadMiddleware"
        else:
            yield m


def environ_get_or_warn(key: str) -> Optional[str]:
    """Get an environment variable or warn that it is not set."""
    value = os.environ.get(key)

    if value is not None:
        return value

    warnings.warn(f"{key} needed for settings was not set in environment")
    return None


class Development(SpectacularSettings, Base):
    """Development configuration."""

    SITE_TITLE = "Local Development"

    SECRET_KEY = "development"

    INSTALLED_APPS: Sequence[str] = (
        # Add daphne for ./manage.py runserver
        # Needs to be there before django.contrib.staticfiles
        "daphne",
        *Base.INSTALLED_APPS,
        "debug_toolbar",
        "drf_spectacular",
        "drf_spectacular_sidecar",
        "django_browser_reload",
        "django_extensions",
    )

    MIDDLEWARE = list(add_dev_middleware(Base.MIDDLEWARE))

    # Debug
    DEBUG = True
    DEBUG_TOOLBAR = True
    DEBUG_AUTH = True

    ALLOWED_HOSTS = os.getenv(
        "ALLOWED_HOSTS", ".localhost,127.0.0.1,[::1]"
    ).split(",")
    # Add the IP you are connecting from to get SQL debug HTTP headers
    INTERNAL_IPS = os.getenv("INTERNAL_IPS", "127.0.0.1").split(",")

    # XXX while developing the new frontend, this is set to
    # match Django's ./manage.py runserver port
    FRONTEND_URL = "http://localhost:8000"

    # Workaround for connecting over .local domain
    # ============================================
    #
    # Add this if you are serving the frontend from a local network host other
    # than localhost, and vite is proxying the backend
    # LOCAL_DOMAIN = "blabla"
    # FRONTEND_URL = f"http://{LOCAL_DOMAIN}.local:3000/"
    # CSRF_COOKIE_SECURE = False
    # CSRF_COOKIE_SAMESITE = "Lax"
    # XXX this might have to revised, not sure what the correct suffix is
    # MEDIA_URL = f"http://{LOCAL_DOMAIN}.local:3000/media/"

    # TODO remove when Svelte frontend is gone
    CSRF_TRUSTED_ORIGINS = (
        # Vite dev
        "http://localhost:3000",
        # Caddy rev proxy
        "http://localhost:5000",
        # See above, add this if you want to serve from another local domain
        # f"http://{LOCAL_DOMAIN}.local:3000",
        # Storybook
        "http://localhost:6006",
        # See above
        # f"http://{LOCAL_DOMAIN}.local:6006",
    )

    # We don't need CELERY_BROKER_URL here because Celery runs tasks
    # immediately.
    CELERY_TASK_ALWAYS_EAGER = True
    # If you need to set the URL, make sure to include the `REDIS_TLS_URL`
    # environment variable. You can also update your `.env` file to achieve
    # this.
    CELERY_BROKER_URL = os.environ.get("REDIS_TLS_URL")

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
    # TODO remove after Svelte frontend is gone
    SESSION_COOKIE_SAMESITE = "Lax"

    # Rest Framework settings for drf-spectacular
    REST_FRAMEWORK = {
        **Base.REST_FRAMEWORK,
        "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    }

    # Settings for slow connection emulation
    SLEEP_MIN_MAX_MS = 200, 500
    # ERROR_RATE_PCT = 20
    CHANNEL_ERROR = 20
    ASGI_APPLICATION = "projectify.test.asgi.error_application"

    # Admins for local logging
    ADMINS = [["Local user", "user@localhost"]]

    # Show preview of all email types
    PREMAIL_PREVIEW = True

    # Enable live reloading
    BROWSER_RELOAD = True

    # Feature flags
    ENABLE_DJANGO_FRONTEND = True

    # Enable template debugging
    TEMPLATES = Base.TEMPLATES
    TEMPLATES[0]["OPTIONS"] = {
        **TEMPLATES[0]["OPTIONS"],
        "debug": True,
    }

    @classmethod
    def pre_setup(cls) -> None:
        """Load environment variables from .env."""
        super().pre_setup()
        load_dotenv()
