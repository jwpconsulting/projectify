# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022, 2023 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Projectify middlewares."""
# https://stackoverflow.com/a/47888695
from typing import (
    Callable,
)

from django.http import (
    HttpRequest,
    HttpResponse,
)

GetResponse = Callable[[HttpRequest], HttpResponse]


class DisableCSRFMiddleware:
    """Dangerous CSRF disable middleware."""

    get_response: GetResponse

    def __init__(self, get_response: GetResponse):
        """Init."""
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Call."""
        # This is insane
        setattr(request, "_dont_enforce_csrf_checks", True)
        response = self.get_response(request)
        return response
