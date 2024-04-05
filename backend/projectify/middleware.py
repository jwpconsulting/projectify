# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022-2024 JWP Consulting GK
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
    Optional,
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


def reverse_proxy(get_response: GetResponse) -> GetResponse:
    """
    Enhance request headers with X-Forwarded-For, if found, for rate limiting.

    It ain't great, and we don't rely on it alone for rate limiting.

    https://devcenter.heroku.com/articles/http-routing#heroku-headers
    Accessed 2024-04-05
    > The X-Forwarded-For, X-Forwarded-By, X-Forwarded-Proto, and X-Forwarded-Host headers are not trusted for security reasons, because it is not possible to know the order in which already existing fields were added (as per Forwarded HTTP Extension).
    > X-Forwarded-For: the originating IP address of the client connecting to the Heroku router

    https://django-ratelimit.readthedocs.io/en/stable/security.html#client-ip-address
    Accessed 2024-04-05
    > Mishandling client IP data creates an IP spoofing vector that allows attackers to circumvent IP ratelimiting entirely

    https://stackoverflow.com/questions/18264304/get-clients-real-ip-address-on-heroku/18517550#18517550
    Accessed 2024-04-05
    > From Jacob, Heroku's Director of Security at the time:
    >> The router doesn't overwrite X-Forwarded-For, but it does guarantee that the real origin will always be the last item in the list.
    > This means that, if you access a Heroku app in the normal way, you will just see your IP address in the X-Forwarded-For header [...]
    > Obviously, this is all we need, so there's a clear and secure solution for getting the client's IP address on Heroku [...]

    https://stackoverflow.com/questions/18264304/get-clients-real-ip-address-on-heroku/37061471#37061471
    Accessed 2024-04-05
    > From a practical standpoint, this IP will likely be reliable most of the time (because most people won't be bothering to spoof their IP). Unfortunately, it's impossible to prevent this sort of spoofing and by the time a request gets to the Heroku router, it's impossible for us to tell if IPs in an X-Forwarded-For chain have been tampered with or not.
    """

    def process_request(request: HttpRequest) -> HttpResponse:
        forwarded_for: Optional[str] = request.META.get("X-Forwarded-For")
        if forwarded_for is not None:
            ips = [ip.strip() for ip in forwarded_for.split(",")]
            request.META["REMOTE_ADDR"] = ips[0]
        return get_response(request)

    return process_request
