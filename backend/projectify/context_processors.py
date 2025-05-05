# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2023 JWP Consulting GK
"""Projectify context processors."""

from typing import Mapping
import os

from django.conf import settings
from typing import Optional

def frontend_url(request: object) -> Mapping[str, str]:
    """Add FRONTEND_URL to context."""
    return {
        "FRONTEND_URL": settings.FRONTEND_URL,
    }
