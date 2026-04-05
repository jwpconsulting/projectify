# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Stats app admin."""

from django.contrib import admin

from projectify.stats.models import DailyCount


@admin.register(DailyCount)
class DailyCountAdmin(admin.ModelAdmin[DailyCount]):
    """Admin for daily counts."""

    list_display = ("name", "date", "count", "created", "modified")
    list_filter = ("date",)
    search_fields = ("name",)
    readonly_fields = ("name", "date", "count", "created", "modified")
    ordering = ("-date", "-count")

    def has_add_permission(self, request: object) -> bool:
        """Prevent adding daily hit counts."""
        del request
        return False

    def has_delete_permission(
        self, request: object, obj: object = None
    ) -> bool:
        """Prevent deleting daily hit counts."""
        del request, obj
        return False
