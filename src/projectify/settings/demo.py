# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Demo settings."""

import secrets
import tempfile
from pathlib import Path

from .base import Base


class Demo(Base):
    """Projectify demo configuration."""

    SITE_TITLE = "Projectify Demo"

    ALLOWED_HOSTS = ["localhost"]

    FRONTEND_URL = "http://localhost:8100"

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        # NOTE: this is a bit flaky and expects the 0th middleware to be
        # the SecurityMiddleware
        *Base.MIDDLEWARE[1:],
    ]

    @classmethod
    def setup(cls) -> None:
        """Set up one-time secret key."""
        super().setup()
        cls.SECRET_KEY = secrets.token_hex(32)
        tmpdir = Path(tempfile.mkdtemp())
        cls.STATIC_ROOT = tmpdir / "staticfiles"
        cls.MEDIA_ROOT = tmpdir / "media"
