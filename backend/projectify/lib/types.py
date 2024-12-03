# SPDX-FileCopyrightText: 2024 JWP Consulting GK
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Types used across apps."""

from django.http import HttpRequest

from django_htmx.middleware import HtmxDetails

from projectify.user.models.user import User


class AuthenticatedHttpRequest(HttpRequest):
    """Authenticated HTTP request."""

    user: User
    htmx: HtmxDetails
