# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
"""Storefront Views."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

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


def download(request: HttpRequest) -> HttpResponse:
    """Serve Download page."""
    markdowntext = (
        get_settings().BASE_DIR / "storefront" / "markdown_en" / "download.md"
    ).read_text()
    context = {"markdowntext": markdowntext}
    return render(request, "storefront/download.html", context)


def credits(request: HttpRequest) -> HttpResponse:
    """Serve Credits page."""
    markdowntext = (
        get_settings().BASE_DIR / "storefront" / "markdown_en" / "credits.md"
    ).read_text()
    context = {"markdowntext": markdowntext}
    return render(request, "storefront/credits.html", context)


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


def solutions_development_teams(request: HttpRequest) -> HttpResponse:
    """Serve development teams solutions page."""
    return render(request, "storefront/solutions/development-teams.html")


def solutions_project_management(request: HttpRequest) -> HttpResponse:
    """Serve project management solutions page."""
    return render(request, "storefront/solutions/project-management.html")


def solutions_academic(request: HttpRequest) -> HttpResponse:
    """Serve academic solutions page."""
    return render(request, "storefront/solutions/academic.html")


def tos(request: HttpRequest) -> HttpResponse:
    """Serve TOS page."""
    return render(request, "storefront/tos.html")


def ethicalads(request: HttpRequest) -> HttpResponse:
    """Show landing."""
    return render(request, "storefront/index.html")
