# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Projectify statistics middleware."""

import datetime
from collections.abc import Sequence
from functools import lru_cache
from typing import Any, Callable, cast

from django.contrib.sitemaps import Sitemap
from django.db import transaction
from django.db.models import F
from django.http import HttpRequest, HttpResponse
from django.utils import timezone

from projectify.urls import sitemaps

from .models import DailyCount

GetResponse = Callable[[HttpRequest], HttpResponse]


@lru_cache(maxsize=1)
def get_sitemap_urls() -> set[str]:
    """Get all URLs from sitemaps, cached."""
    sitemap_urls: set[str] = set()
    for sitemap_class in sitemaps.values():
        sitemap: Sitemap = sitemap_class()
        items = cast(Sequence[Any], sitemap.items())
        for item in items:
            url: str = sitemap.location(item)
            sitemap_urls.add(url)
    return sitemap_urls


def track_hit(path: str) -> None:
    """Track a hit for a given path."""
    sitemap_urls = get_sitemap_urls()
    if path not in sitemap_urls:
        return
    today = timezone.now().astimezone(datetime.timezone.utc).date()
    with transaction.atomic():
        hit_count_qs = DailyCount.objects.filter(
            name=path, date=today
        ).select_for_update()

        if hit_count_qs.exists():
            hit_count_qs.update(count=F("count") + 1)
        else:
            DailyCount.objects.create(name=path, date=today, count=1)


def count_stats(get_response: GetResponse) -> GetResponse:
    """Middleware to track daily hit counts for sitemap URLs."""

    def process_request(request: HttpRequest) -> HttpResponse:
        response = get_response(request)
        track_hit(request.path)
        return response

    return process_request
