# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Clean up old user events."""

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from projectify.lib.settings import get_settings
from projectify.user.models import UserEvent


class Command(BaseCommand):
    """Clean old user events."""

    help = "Clean old user events according to retention period"

    def handle(self, *args: object, **options: object) -> None:
        """Handle."""
        del args, options
        settings = get_settings()
        cutoff = now() - timedelta(
            seconds=settings.USER_EVENT_RETENTION_PERIOD
        )
        old = UserEvent.objects.filter(created__lt=cutoff)
        old.delete()
