# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2021-2024 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Development settings."""

import logging
import os
from collections.abc import (
    Iterable,
    Sequence,
)
from pathlib import Path
from typing import Optional

from dotenv import (
    load_dotenv,
)

from projectify.lib.settings import populate_production_middleware

from .base import Base
from .spectacular import SpectacularSettings

logger = logging.getLogger(__name__)


def add_dev_middleware(middleware: Sequence[str]) -> Iterable[str]:
    """Add the debug toolbar to debug middleware."""
    gzip_middleware = "django.middleware.gzip.GZipMiddleware"
    for m in middleware:
        if m == gzip_middleware:
            yield m
            yield "debug_toolbar.middleware.DebugToolbarMiddleware"
            yield "projectify.middleware.microsloth"
            yield "projectify.middleware.errorsloth"
        else:
            yield m


def environ_get_or_warn(key: str) -> Optional[str]:
    """Get an environment variable or warn that it is not set."""
    value = os.environ.get(key)

    if value is not None:
        return value

    logger.warn(f"{key} needed for settings was not set in environment")
    return None


class Development(SpectacularSettings, Base):
    """Development configuration."""

    SITE_TITLE = "Local Development"

    SECRET_KEY = "development"

    INSTALLED_APPS: Sequence[str] = (
        *Base.INSTALLED_APPS,
        "debug_toolbar",
        "drf_spectacular",
        "drf_spectacular_sidecar",
    )

    MIDDLEWARE = list(add_dev_middleware(Base.MIDDLEWARE))

    # Debug
    DEBUG = True
    DEBUG_TOOLBAR = True
    ALLOWED_HOSTS = os.getenv(
        "ALLOWED_HOSTS", ".localhost,127.0.0.1,[::1]"
    ).split(",")
    # Add the IP you are connecting from to get SQL debug HTTP headers
    INTERNAL_IPS = os.getenv("INTERNAL_IPS", "127.0.0.1").split(",")

    FRONTEND_URL = "http://localhost:3000"

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

    # If all requests are proxied through vite, I'm not sure if this is
    # relevant or not:
    CORS_ALLOWED_ORIGINS = (
        # Vite dev
        "http://localhost:3000",
        # Storybook
        "http://localhost:6006",
    )
    # On the other hand, local tests showed me that CSRF_TRUSTED_ORIGINS has to
    # be adjusted when serving from another local domain
    CSRF_TRUSTED_ORIGINS = (
        # Vite dev
        "http://localhost:3000",
        # See above, add this if you want to serve from another local domain
        # f"http://{LOCAL_DOMAIN}.local:3000",
        # Storybook
        "http://localhost:6006",
        # See above
        # f"http://{LOCAL_DOMAIN}.local:6006",
    )

    CELERY_TASK_ALWAYS_EAGER = True
    # TODO if celery is eager, a broker should not be necessary, right?
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
    SESSION_COOKIE_SAMESITE = "Lax"

    # Rest Framework settings for drf-spectacular
    REST_FRAMEWORK = {
        **Base.REST_FRAMEWORK,
        "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    }

    # Settings for slow connection emulation
    SLEEP_MIN_MAX_MS = 200, 500
    ERROR_RATE_PCT = None
    CHANNEL_ERROR = 15, 50
    ASGI_APPLICATION = "projectify.test.asgi.error_application"

    @classmethod
    def pre_setup(cls) -> None:
        """Load environment variables from .env."""
        super().pre_setup()
        load_dotenv()


class DevelopmentNix(Development):
    """Preliminary configuration for poetry2nix packaged backend."""

    SITE_TITLE = "Projectify-Backend (nix)"

    STORAGES = {
        **Development.STORAGES,
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

    # Use middelware from production for added realism
    MIDDLEWARE = list(populate_production_middleware(Base.MIDDLEWARE))

    # We need to inject the static root path during the nix build process
    STATIC_ROOT = Path(os.environ["STATIC_ROOT"])

    # No need for debug or debug libs, for added realism
    DEBUG = False
    INSTALLED_APPS = Base.INSTALLED_APPS
    SERVE_SPECTACULAR = False
    DEBUG_TOOLBAR = False
