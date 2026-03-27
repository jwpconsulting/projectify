# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""
Blog RSS feeds.

See
https://docs.djangoproject.com/en/6.0/ref/contrib/syndication/
"""

from datetime import datetime
from typing import Optional

from django.contrib.syndication.views import Feed
from django.db.models import Model, QuerySet
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .models import Post
from .selectors.post import post_list_published


class LatestPostsFeed(Feed):
    """RSS feed for latest blog posts."""

    title = _("Projectify Blog")
    link = reverse_lazy("blog:post_list")
    description = _("Latest posts from the Projectify blog")

    def items(self) -> QuerySet[Post]:
        """Return latest published posts."""
        return post_list_published(with_body=True)[:10]

    # in the Django type stubs, the return type is
    # SafeText
    def item_title(self, item: Model) -> str:  # type: ignore[override]
        """Return post title."""
        if not isinstance(item, Post):
            raise ValueError("Expected Post, got {}".format(type(item)))
        return item.title

    def item_description(self, item: Model) -> str:
        """Return post description."""
        if not isinstance(item, Post):
            raise ValueError("Expected Post, got {}".format(type(item)))
        if not item.body:
            raise ValueError("Expected post to have body")
        return item.body.get_plain_text_content()

    def item_pubdate(self, item: Post) -> Optional[datetime]:
        """Return publication date."""
        return datetime.combine(item.published, datetime.min.time())

    def item_author_name(self, item: Post) -> str:
        """Return author name."""
        return item.author

    def item_link(self, item: Model) -> str:
        """Return link to post."""
        if not isinstance(item, Post):
            raise ValueError("Expected Post, got {}".format(type(item)))
        return item.get_absolute_url()
