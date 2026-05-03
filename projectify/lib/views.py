# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""View decorators."""

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import RedirectView

from projectify.lib.types import DjangoView, LoggedInViewP


def platform_view(func: LoggedInViewP) -> LoggedInViewP:
    """
    Wrap view in login_required.

    This makes it easier to add required decorators or other things to views
    that are part of the platform, i.e., pages that require the user to be
    logged in.

    Usage

    from django.http import HttpResponse
    from projectify.lib.types import AuthenticatedHttpRequest
    from projectify.lib.views import platform_view
    @platform_view
    def method(request: AuthenticatedHttpRequest) -> HttpResponse:
        pass

    TODO, implement this

    @platform_view(require_methods=["GET", "POST"])
    def method(request: AuthenticatedHttpRequest) -> HttpResponse:
        pass

    This validates request.method in ["GET", "POST"]
    """
    return login_required(func)


def permanent_redirect(urlname: str) -> DjangoView:
    """Return a permanent redirect view function."""
    return RedirectView.as_view(url=reverse_lazy(urlname), permanent=True)
