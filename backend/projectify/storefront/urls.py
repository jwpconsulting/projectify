# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
"""Storefront urlpatterns."""

from django.urls import include, path

from projectify.storefront.views import (
    accessibility,
    contact_us,
    credits,
    free_software,
    index,
    pricing,
    privacy,
    security_disclose,
    security_general,
    solutions_detail,
    solutions_index,
    tos,
)

app_name = "storefront"

solution_patterns = [
    path("", solutions_index, name="list"),
    path("<slug:page>/", solutions_detail, name="detail"),
]

urlpatterns = [
    path("accessibility/", accessibility),
    path("contact-us/", contact_us),
    path("free-software/", free_software),
    path("credits/", credits),
    path("security/general/", security_general),
    path("security/disclose/", security_disclose),
    path("tos/", tos),
    path("pricing/", pricing),
    path("privacy/", privacy),
    path("solutions/", include((solution_patterns, "solutions"))),
    path("", index),
]
