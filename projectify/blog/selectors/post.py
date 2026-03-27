# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Blog post selectors."""

from typing import Optional

from django.db.models import QuerySet
from django.utils import timezone

from ..models import Post


def post_list_published() -> QuerySet[Post]:
    """Return published posts without content."""
    today = timezone.now().date()
    return Post.objects.filter(published__lte=today).defer("body")


def post_find_by_slug(*, slug: str) -> Optional[Post]:
    """Find a post by slug."""
    today = timezone.now().date()
    return (
        Post.objects.filter(slug=slug, published__lte=today)
        .select_related("body")
        .first()
    )
