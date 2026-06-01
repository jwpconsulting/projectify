# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2023 JWP Consulting GK
"""Projectify context processors."""

from typing import Mapping

from django.conf import settings
from django.http import HttpRequest


def frontend_url(request: object) -> Mapping[str, str]:
    """Add FRONTEND_URL to context."""
    return {"FRONTEND_URL": settings.FRONTEND_URL}


def show_go_to_dashboard(request: HttpRequest) -> Mapping[str, bool]:
    """Tell header nav that it can show "Go to dashboard"."""
    match = request.resolver_match
    if not match:
        return {}
    if not match.app_names:
        return {}
    return {"show_go_to_dashboard": match.app_names[0] != "dashboard"}
