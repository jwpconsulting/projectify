# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2022, 2023 JWP Consulting GK
"""Test settings."""

try:
    from dotenv import load_dotenv
except ImportError as e:
    raise RuntimeError(
        "dotenv was not found. Please check if dev dependencies have been installed"
    ) from e

from .base import Base
from .spectacular import SpectacularSettings


class Test(SpectacularSettings, Base):
    """Test configuration."""

    INSTALLED_APPS = (
        *Base.INSTALLED_APPS,
        "drf_spectacular",
    )

    SITE_TITLE = "Projectify Pytest"

    # TODO populate me
    SECRET_KEY = "test"

    FRONTEND_URL = "https://example.com"

    # Email
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    EMAIL_EAGER = True

    # Celery
    CELERY_BROKER_URL = "memory://"

    # django-ratelimit
    RATELIMIT_ENABLE = False

    # Rest Framework settings for drf-spectacular
    REST_FRAMEWORK = {
        **Base.REST_FRAMEWORK,
        "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    }

    # Enable premail preview for testing
    PREMAIL_PREVIEW = True

    @classmethod
    def pre_setup(cls) -> None:
        """Load environment variables from .env."""
        super().pre_setup()
        load_dotenv()


class TestCollectstatic(Test):
    """Settings to test static file collection needed for whitenoise."""

    STORAGES = {
        **Base.STORAGES,
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
