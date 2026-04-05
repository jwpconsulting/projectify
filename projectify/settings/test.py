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


class Test(Base):
    """Test configuration."""

    SITE_TITLE = "Projectify Pytest"

    # TODO populate me
    SECRET_KEY = "test"

    FRONTEND_URL = "https://example.com"

    # django_sendfile2 settings
    SENDFILE_BACKEND = "django_sendfile.backends.simple"

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

    @classmethod
    def setup(cls) -> None:
        """Set up mock OAuth app credentials."""
        super().setup()
        cls.SOCIALACCOUNT_PROVIDERS["github"]["APPS"].append(
            {"client_id": "TEST", "secret": "TEST"}
        )

        cls.SOCIALACCOUNT_PROVIDERS["google"]["APPS"].append(
            {"client_id": "TEST", "secret": "TEST"}
        )
