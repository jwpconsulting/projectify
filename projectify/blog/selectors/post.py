# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Blog post selectors."""

from typing import Optional

from django.db.models import QuerySet
from django.utils import timezone

from ..models import Post


def post_list_published(
    *, with_body: bool = False, exclude: Optional[Post] = None
) -> QuerySet[Post]:
    """Return published posts without content."""
    today = timezone.now().date()
    posts = Post.objects.filter(published__lte=today)
    if exclude:
        posts = posts.exclude(pk=exclude.pk)
    if with_body:
        return posts.select_related("body")
    else:
        return posts.defer("body")


def post_list_published_with_body() -> QuerySet[Post]:
    """Return published posts with content for RSS feed."""
    today = timezone.now().date()
    return Post.objects.filter(published__lte=today).select_related("body")


def post_find_by_slug(*, slug: str) -> Optional[Post]:
    """Find a post by slug."""
    today = timezone.now().date()
    return (
        Post.objects.filter(slug=slug, published__lte=today)
        .select_related("body")
        .first()
    )
