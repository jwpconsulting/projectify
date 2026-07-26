# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022-2024 JWP Consulting GK
"""Projectify middlewares."""

import logging
from typing import Callable

from django.http import HttpRequest, HttpResponse

from projectify.lib.settings import get_settings

logger = logging.getLogger(__name__)

GetResponse = Callable[[HttpRequest], HttpResponse]


def reverse_proxy(get_response: GetResponse) -> GetResponse:
    """
    Enhance request headers with X-Forwarded-For, if found, for rate limiting.

    Projectify depends on Caddy as reverse proxy. Caddy passes the client
    IP in the `X-Forwarded-For` header field:

    > By default, Caddy passes through incoming headers—including Host—to
    > the backend without modifications, with three exceptions:
    > * It sets or augments the X-Forwarded-For header field.
    > * […]
    >
    > For these X-Forwarded-* headers, by default, the proxy will ignore their
    > values from incoming requests, to prevent spoofing.

    See
    <https://caddyserver.com/docs/caddyfile/directives/reverse_proxy#headers>

    To tell Caddy to not ignore X-Forwarded-For in client requests, you can
    allow certain proxy names in X-Forwarded-For with the `trusted_proxies`
    setting.
    See https://caddyserver.com/docs/caddyfile/options#trusted-proxies

    At the time of writing, Caddy for Projectify
    does not use the trusted_proxies setting.
    """
    settings = get_settings()

    def process_request(request: HttpRequest) -> HttpResponse:
        match request.headers.get("X-Forwarded-For"):
            case str() as forwarded_for:
                ips = [ip.strip() for ip in forwarded_for.split(",")]
                if len(ips) == 0:
                    raise ValueError(
                        "X-Forwarded-For was specified, but no list of "
                        f"IPs was given: {forwarded_for}"
                    )
                request.META["REMOTE_ADDR"] = ips[0]
            # Lazily assume that DEBUG == False -> Projectify runs inside
            # gunicorn
            case None if settings.DEBUG is False:
                logger.debug(
                    "No X-Forwarded-For in request headers. Using REMOTE_ADDR %s",
                    request.META["REMOTE_ADDR"],
                )
            case None:
                pass
        return get_response(request)

    return process_request
