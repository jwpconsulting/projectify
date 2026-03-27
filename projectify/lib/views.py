# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""View decorators."""

from typing import Any, Protocol

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import RedirectView

from projectify.lib.types import AuthenticatedHttpRequest


class LoggedInViewP(Protocol):
    """Django view method that takes an AuthenticatedHttpRequest."""

    def __call__(
        self, request: AuthenticatedHttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        """Take a request and respond."""
        ...


def platform_view(func: LoggedInViewP) -> LoggedInViewP:
    """
    Wrap view in login_required.

    This makes it easier to add required decorators or other things to views
    that are part of the platform, i.e., pages that require the user to be
    logged in.
    """
    return login_required(func)


class View(Protocol):
    """Generic Django view type."""

    def __call__(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        """Return response."""
        ...


def permanent_redirect(urlname: str) -> View:
    """Return a permanent redirect view function."""
    return RedirectView.as_view(url=reverse_lazy(urlname), permanent=True)
