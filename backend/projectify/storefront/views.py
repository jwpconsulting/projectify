# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
"""Storefront Views."""

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from projectify.lib.settings import get_settings


def accessibility(request: HttpRequest) -> HttpResponse:
    """Serve Accessibility page."""
    markdowntext = (
        get_settings().BASE_DIR
        / "storefront"
        / "markdown_en"
        / "accessibility.md"
    ).read_text()
    context = {"markdowntext": markdowntext}
    return render(request, "storefront/accessibility.html", context)


def contact_us(request: HttpRequest) -> HttpResponse:
    """Serve Contact us page."""
    markdowntext = (
        get_settings().BASE_DIR
        / "storefront"
        / "markdown_en"
        / "contact-us.md"
    ).read_text()
    context = {"markdowntext": markdowntext}
    return render(request, "storefront/contact_us.html", context)


def credits(request: HttpRequest) -> HttpResponse:
    """Serve Credits page."""
    return render(request, "storefront/credits.html")


def index(request: HttpRequest) -> HttpResponse:
    """Serve landing page."""
    return render(request, "storefront/index.html")


def free_software(request: HttpRequest) -> HttpResponse:
    """Serve Free Software page."""
    markdowntext = (
        get_settings().BASE_DIR
        / "storefront"
        / "markdown_en"
        / "free-software.md"
    ).read_text()
    context = {"markdowntext": markdowntext}
    return render(request, "storefront/free_software.html", context)


def pricing(request: HttpRequest) -> HttpResponse:
    """Serve Pricing page."""
    return render(request, "storefront/pricing.html")


def privacy(request: HttpRequest) -> HttpResponse:
    """Serve Privacy page."""
    return render(request, "storefront/privacy.html")


def security_disclose(request: HttpRequest) -> HttpResponse:
    """Serve Security Disclose page."""
    markdowntext = (
        get_settings().BASE_DIR
        / "storefront"
        / "markdown_en"
        / "security"
        / "disclose.md"
    ).read_text()
    context = {"markdowntext": markdowntext}
    return render(request, "storefront/security/disclose.html", context)


def security_general(request: HttpRequest) -> HttpResponse:
    """Serve Security Genaral page."""
    markdowntext = (
        get_settings().BASE_DIR
        / "storefront"
        / "markdown_en"
        / "security"
        / "general.md"
    ).read_text()
    context = {"markdowntext": markdowntext}
    return render(request, "storefront/security/general.html", context)


def solutions_index(request: HttpRequest) -> HttpResponse:
    """Serve Solutions Index page."""
    return render(request, "storefront/solutions/solutions_index.html")


def solutions_detail(request: HttpRequest, page: str) -> HttpResponse:
    """Serve Solutions Detail page."""
    match page:
        case "development-teams":
            return render(
                request, "storefront/solutions/development-teams.html"
            )
        case "research":
            return render(request, "storefront/solutions/research.html")
        case "project-management":
            return render(
                request, "storefront/solutions/project-management.html"
            )
        case "academic":
            return render(request, "storefront/solutions/academic.html")
        case "remote-work":
            return render(request, "storefront/solutions/remote-work.html")
        case "personal-use":
            return render(request, "storefront/solutions/personal-use.html")
        case _:
            # TODO:Add proper solutions detail route implementations
            raise Http404(_("Solution page does not exist."))


def tos(request: HttpRequest) -> HttpResponse:
    """Serve TOS page."""
    return render(request, "storefront/tos.html")


def ethicalads(request: HttpRequest) -> HttpResponse:
    """Show landing."""
    return render(request, "storefront/index.html")
