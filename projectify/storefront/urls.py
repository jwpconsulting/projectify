# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
"""Storefront urlpatterns."""

from django.urls import include, path

from projectify.lib.views import permanent_redirect
from projectify.storefront.views import (
    accessibility,
    contact_us,
    credits,
    download,
    ethicalads,
    free_software,
    index,
    pricing,
    privacy,
    security_disclose,
    security_general,
    tos,
)

app_name = "storefront"

security_patterns = [
    path("general", security_general, name="general"),
    path("disclose", security_disclose, name="disclose"),
]

urlpatterns = [
    path("accessibility", accessibility, name="accessibility"),
    path("contact-us", contact_us, name="contact_us"),
    path("download", download, name="download"),
    path("ethicalads", ethicalads, name="ethicalads"),
    path("free-software", free_software, name="free_software"),
    path("credits", credits, name="credits"),
    path("security/", include((security_patterns, "security"))),
    path("tos", tos, name="tos"),
    path("pricing", pricing, name="pricing"),
    path("privacy", privacy, name="privacy"),
    # Former solutions views
    *(
        path(p, permanent_redirect("storefront:landing"))
        for p in [
            "solutions",
            "solutions/",
            "solutions/development-teams",
            "solutions/project-management",
            "solutions/academic",
            "solutions/personal-use",
            "solutions/remote-work",
            "solutions/research",
            "solutions/project-management/",
            "solutions/development-teams/",
            "solutions/academic/",
        ]
    ),
    path("", index, name="landing"),
]
