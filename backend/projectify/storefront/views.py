# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
import os

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def accessibility(request: HttpRequest):
    markdowntext = open(
        os.path.join(
            os.path.dirname(__file__),
            "../../../frontend/src/messages/en/accessibility.md",
        )
    ).read()
    context = {"markdowntext": markdowntext}
    return render(request, "storefront/accessibility.html", context)


def contact_us(request: HttpRequest):
    pass


def credits(request: HttpRequest):
    pass


def ethicalads(request: HttpRequest):
    pass


def free_software(request: HttpRequest):
    pass


def pricing(request: HttpRequest) -> HttpResponse:
    pass


def privacy(request: HttpRequest) -> HttpResponse:
    pass


def security_disclose(request: HttpRequest) -> HttpResponse:
    pass


def escurity_general(request: HttpRequest) -> HttpResponse:
    pass


def solutions_index(request: HttpRequest) -> HttpResponse:
    pass


def solutions_detail(request: HttpRequest, page: str) -> HttpResponse:
    pass


def tos(request: HttpRequest) -> HttpResponse:
    pass
