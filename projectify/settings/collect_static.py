# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""Settings used to run ./manage.py collectstatic."""

import os
from pathlib import Path

from .base import Base


class CollectStatic(Base):
    """Only contain the settings necessary to run ./manage.py collectstatic."""

    STATIC_ROOT = Path(os.environ["STATIC_ROOT"])

    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        # Caddy serves static files
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
        },
    }
