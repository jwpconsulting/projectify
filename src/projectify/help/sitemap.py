# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Sitemap for help."""

from django.contrib import sitemaps
from django.urls import reverse

from projectify.help.views import HELP_TOPICS


class HelpSitemap(sitemaps.Sitemap):
    """Sitemap for help URLs."""

    priority = 0.5
    changefreq = "weekly"

    def items(self) -> list[str]:
        """
        Return item names.

        See names in help/urls.py.
        """
        # NOTE you may have to update this when you add more URLs to
        # help/urls.py
        return [
            "help:list",
            *[f"help:topic:{topic}" for topic in HELP_TOPICS.keys()],
        ]

    def location(self, item: str) -> str:  # type: ignore
        """Retrieve location for item."""
        return reverse(item)
