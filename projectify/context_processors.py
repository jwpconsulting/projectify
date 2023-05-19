"""Projectify context processors."""
from typing import (
    Mapping,
)

from django.conf import (
    settings,
)


def frontend_url(request: object) -> Mapping[str, str]:
    """Add FRONTEND_URL to context."""
    return {
        "FRONTEND_URL": settings.FRONTEND_URL,
    }
