# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
"""Storefront Views."""

import os

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def accessibility(request: HttpRequest):
    """Serve Accessibility page."""
    markdowntext = open(
        os.path.join(
            os.path.dirname(__file__),
            "../../../frontend/src/messages/en/accessibility.md",
        )
    ).read()
    context = {"markdowntext": markdowntext}
    return render(request, "storefront/accessibility.html", context)


def contact_us(request: HttpRequest):
    """Serve Contact us page."""
    pass


def credits(request: HttpRequest):
    """Serve Credits page."""
    pass


def ethicalads(request: HttpRequest):
    """Serve Ethicalads page."""
    pass


def free_software(request: HttpRequest):
    """Serve Free Software page."""
    pass


def pricing(request: HttpRequest) -> HttpResponse:
    """Serve Pricing page."""
    pass


def privacy(request: HttpRequest) -> HttpResponse:
    """Serve Privacy page."""
    pass


def security_disclose(request: HttpRequest) -> HttpResponse:
    """Serve Security Disclose page."""
    pass


def escurity_general(request: HttpRequest) -> HttpResponse:
    """Serve Escurity Genaral page."""
    pass


def solutions_index(request: HttpRequest) -> HttpResponse:
    """Serve Solutions Index page."""
    pass


def solutions_detail(request: HttpRequest, page: str) -> HttpResponse:
    """Serve Solutions Detail page."""
    pass


def tos(request: HttpRequest) -> HttpResponse:
    """Serve TOS page."""
    pass
