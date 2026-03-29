# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Demo settings."""

import os
import secrets
from pathlib import Path

from projectify.settings.base import Base


class Demo(Base):
    """Projectify demo configuration."""

    SITE_TITLE = "Projectify Demo"

    ALLOWED_HOSTS = ["localhost"]

    # TODO remove when Svelte frontend is gone
    FRONTEND_URL = "http://localhost:8100"

    # Static files
    # We allow overriding this value in case the static files come prebuilt,
    # for example in a container, and an exact path is contained in
    # the STATIC_ROOT environment variable
    STATIC_ROOT = (
        Path(os.environ["STATIC_ROOT"])
        if "STATIC_ROOT" in os.environ
        else Base.STATIC_ROOT
    )

    @classmethod
    def setup(cls) -> None:
        """Set up one-time secret key."""
        super().setup()
        cls.SECRET_KEY = secrets.token_hex(32)
