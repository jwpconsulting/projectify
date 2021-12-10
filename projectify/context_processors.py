"""Projectify context processors."""
from django.conf import (
    settings,
)


def frontend_url(request):
    """Add FRONTEND_URL to context."""
    return {
        "FRONTEND_URL": settings.FRONTEND_URL,
    }
