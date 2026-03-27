# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Sitemap for blog app."""

from datetime import datetime
from typing import Optional, Union

from django.contrib import sitemaps
from django.urls import reverse

from projectify.blog.models import Post


class BlogSitemap(sitemaps.Sitemap):
    """Sitemap for blog URLs."""

    priority = 0.5
    changefreq = "weekly"

    def items(self) -> list[str | Post]:
        """
        Return item names and post objects.

        See names in blog/urls.py.
        """
        posts = list(Post.objects.all())
        return ["blog:post_list", *posts]

    def location(self, obj: Union[str, Post]) -> str:  # type: ignore[override]
        """Retrieve location for item."""
        match obj:
            case str():
                return reverse(obj)
            case Post(slug=slug):
                return reverse("blog:post_detail", kwargs={"slug": slug})

    def lastmod(self, obj: Union[str, Post]) -> Optional[datetime]:
        """Return last modification date for posts."""
        match obj:
            case str():
                return None
            case Post(modified=modified):
                return modified
