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


def clean_middleware(middleware: list[str]) -> list[str]:
    """
    Remove whitenoise from middleware list.

    Whitenoise needs you to create the staticfiles directory,
    which isn't too relevant for testing.
    """
    return [
        m
        for m in middleware
        if m not in ["whitenoise.middleware.WhiteNoiseMiddleware"]
    ]


class Test(Base):
    """Test configuration."""

    SITE_TITLE = "Projectify Pytest"

    # TODO populate me
    SECRET_KEY = "test"

    FRONTEND_URL = "https://example.com"

    # Middleware
    MIDDLEWARE = clean_middleware(Base.MIDDLEWARE)

    # Email
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    # django-ratelimit
    RATELIMIT_ENABLE = False

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
