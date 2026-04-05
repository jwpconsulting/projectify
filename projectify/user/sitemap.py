# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Sitemap for user app."""

from django.contrib import sitemaps
from django.urls import reverse


class UserSitemap(sitemaps.Sitemap):
    """Sitemap for user URLs."""

    priority = 0.5
    changefreq = "weekly"

    def items(self) -> list[str]:
        """Return list of URL names."""
        return [
            "users:log-in",
            "users:sign-up",
            "users:request-password-reset",
        ]

    def location(self, obj: str) -> str:  # type: ignore[override]
        """Return the URL for the item."""
        return reverse(obj)
