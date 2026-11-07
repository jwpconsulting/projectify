# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Test user app management commands."""

from datetime import datetime, timedelta

from django.core.management import call_command

import pytest

from projectify.lib.settings import get_settings

from ..models import UserEvent

pytestmark = pytest.mark.django_db


def test_user_event_clean(user_event: UserEvent, now: datetime) -> None:
    """Test user event cleaning."""
    settings = get_settings()
    assert UserEvent.objects.count() == 1
    call_command("user_event_clean")
    assert UserEvent.objects.count() == 1
    user_event.created = now - timedelta(
        seconds=settings.USER_EVENT_RETENTION_PERIOD
    )
    user_event.save()
    call_command("user_event_clean")
    assert UserEvent.objects.count() == 0
