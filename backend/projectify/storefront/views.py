# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
"""Storefront Views."""

import os

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def accessibility(request: HttpRequest) -> HttpResponse:
    """Serve Accessibility page."""
    markdowntext = open(
        os.path.join(
            os.path.dirname(__file__),
            "../../../frontend/src/messages/en/accessibility.md",
        )
    ).read()
    context = {"markdowntext": markdowntext}
    return render(request, "storefront/accessibility.html", context)


def contact_us(request: HttpRequest) -> HttpResponse:
    """Serve Contact us page."""
    markdowntext = open(
        os.path.join(
            os.path.dirname(__file__),
            "../../../frontend/src/messages/en/contact-us.md",
        )
    ).read()
    context = {"markdowntext": markdowntext}
    return render(request, "storefront/contact_us.html", context)


def credits(request: HttpRequest) -> HttpResponse:
    """Serve Credits page."""
    return render(request, "storefront/credits.html")


def ethicalads(request: HttpRequest) -> HttpResponse:
    """Serve Ethicalads page."""
    return HttpResponse("TODO")


def free_software(request: HttpRequest) -> HttpResponse:
    """Serve Free Software page."""
    markdowntext = open(
        os.path.join(
            os.path.dirname(__file__),
            "../../../frontend/src/messages/en/free-software.md",
        )
    ).read()
    context = {"markdowntext": markdowntext}
    return render(request, "storefront/free_software.html", context)


def pricing(request: HttpRequest) -> HttpResponse:
    """Serve Pricing page."""
    return HttpResponse("TODO")


def privacy(request: HttpRequest) -> HttpResponse:
    """Serve Privacy page."""
    return HttpResponse("TODO")


def security_disclose(request: HttpRequest) -> HttpResponse:
    """Serve Security Disclose page."""
    return HttpResponse("TODO")


def escurity_general(request: HttpRequest) -> HttpResponse:
    """Serve Escurity Genaral page."""
    return HttpResponse("TODO")


def solutions_index(request: HttpRequest) -> HttpResponse:
    """Serve Solutions Index page."""
    return HttpResponse("TODO")


def solutions_detail(request: HttpRequest, page: str) -> HttpResponse:
    """Serve Solutions Detail page."""
    return HttpResponse("TODO")


def tos(request: HttpRequest) -> HttpResponse:
    """Serve TOS page."""
    return HttpResponse("TODO")
