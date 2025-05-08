# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
"""Storefront urlpatterns."""

from django.urls import path

from projectify.storefront.views import (
    accessibility,
    contact_us,
    free_software,
)

urlpatterns = [
    path("accessibility/", accessibility),
    path("contact-us/", contact_us),
    path("free-software/", free_software),
]
