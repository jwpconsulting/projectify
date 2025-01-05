# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""General dashboard views."""

from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from projectify.lib.types import AuthenticatedHttpRequest


def redirect_to_dashboard(_request: AuthenticatedHttpRequest) -> HttpResponse:
    """Redirect to dashboard."""
    return redirect(reverse("dashboard:workspaces:list"))
