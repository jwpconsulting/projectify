# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""
Sitemap for storefront.

See
https://docs.djangoproject.com/en/6.0/ref/contrib/sitemaps/#sitemap-for-static-views
"""

from django.contrib import sitemaps
from django.urls import reverse


class StorefrontSitemap(sitemaps.Sitemap):
    """Sitemap for storefront URLs."""

    priority = 0.5
    changefreq = "daily"

    def items(self) -> list[str]:
        """
        Return item names.

        See names in storefront/urls.py.
        """
        return [
            "storefront:landing",
            "storefront:accessibility",
            "storefront:contact_us",
            "storefront:download",
            "storefront:ethicalads",
            "storefront:free_software",
            "storefront:credits",
            "storefront:tos",
            "storefront:pricing",
            "storefront:privacy",
            "storefront:security:general",
            "storefront:security:disclose",
            "storefront:solutions:list",
            "storefront:solutions:development_teams",
            "storefront:solutions:project_management",
            "storefront:solutions:academic",
        ]

    def location(self, item: str) -> str:  # type: ignore
        """Retrieve location for item."""
        return reverse(item)
