# SPDX-FileCopyrightText: 2024 JWP Consulting GK
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Types used across apps."""

from collections.abc import Sequence
from typing import Any, Protocol, Union

from django.http import HttpRequest, HttpResponse
from django.urls import URLPattern, URLResolver

from projectify.user.models import User

from .htmx import HtmxDetails


class AuthenticatedHttpRequest(HttpRequest):
    """Authenticated HTTP request."""

    user: User
    htmx: HtmxDetails


UrlPatterns = Sequence[Union[URLResolver, URLPattern]]


class LoggedInViewP(Protocol):
    """Django view method that takes an AuthenticatedHttpRequest."""

    def __call__(
        self, request: AuthenticatedHttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        """Take a request and respond."""
        ...


class DjangoView(Protocol):
    """Generic Django view type."""

    def __call__(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        """Return response."""
        ...


class SupportsGetAbsoluteUrl(Protocol):
    """Protocol for objects that have the get_absolute_url method."""

    def get_absolute_url(self) -> str:
        """Return a URL for this model instance."""
        ...
