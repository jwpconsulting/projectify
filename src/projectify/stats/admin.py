# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Stats app admin."""

from datetime import date, timedelta

from django.contrib import admin
from django.db.models import Sum
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import URLPattern, path
from django.utils.translation import gettext_lazy as _

from projectify.lib.admin import ReadOnlyAdmin
from projectify.stats.models import DailyCount


@admin.register(DailyCount)
class DailyCountAdmin(ReadOnlyAdmin[DailyCount], admin.ModelAdmin[DailyCount]):
    """Admin for daily counts."""

    list_display = ("name", "date", "count", "created", "modified")
    list_filter = ("date",)
    search_fields = ("name",)
    readonly_fields = ("name", "date", "count", "created", "modified")
    ordering = ("-date", "-count")

    def get_urls(self) -> list[URLPattern]:
        """Add summary stats URL."""
        urls = super().get_urls()
        custom = [
            path(
                "summary/",
                self.admin_site.admin_view(self.stats_summary_view),
                name="stats_dailycount_summary",
            )
        ]
        return custom + urls

    def stats_summary_view(self, request: HttpRequest) -> HttpResponse:
        """Render summarized stats page."""
        today = date.today()
        per_page_31 = (
            DailyCount.objects.filter(date__gte=today - timedelta(days=31))
            .values("name")
            .annotate(total=Sum("count"))
            .order_by("-total")
        )
        per_day_31 = (
            DailyCount.objects.filter(date__gte=today - timedelta(days=31))
            .values("date")
            .annotate(total=Sum("count"))
            .order_by("-date")
        )

        context = {
            **self.admin_site.each_context(request),
            "title": _("Summary"),
            "per_page_31": list(per_page_31),
            "per_day_31": list(per_day_31),
            "opts": self.model._meta,
        }
        return render(request, "admin/stats/dailycount/summary.html", context)
