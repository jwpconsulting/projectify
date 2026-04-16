# SPDX-FileCopyrightText: 2024 JWP Consulting GK
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Types used across apps."""

from collections.abc import Sequence
from typing import Union

from django.http import HttpRequest
from django.urls import URLPattern, URLResolver

from projectify.user.models import User

from .htmx import HtmxDetails


class AuthenticatedHttpRequest(HttpRequest):
    """Authenticated HTTP request."""

    user: User
    htmx: HtmxDetails


UrlPatterns = Sequence[Union[URLResolver, URLPattern]]
