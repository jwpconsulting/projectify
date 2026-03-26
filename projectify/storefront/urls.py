# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
"""Storefront urlpatterns."""

from django.urls import include, path, reverse_lazy
from django.views.generic import RedirectView

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
    solutions_academic,
    solutions_development_teams,
    solutions_index,
    solutions_project_management,
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
    # Solutions
    path("solutions", solutions_index, name="solutions-list"),
    path(
        "solutions/",
        RedirectView.as_view(url=reverse_lazy("storefront:solutions-list")),
    ),
    path(
        "solutions/development-teams",
        solutions_development_teams,
        name="solutions-development-teams",
    ),
    path(
        "solutions/project-management",
        solutions_project_management,
        name="solutions-project-management",
    ),
    path("solutions/academic", solutions_academic, name="solutions-academic"),
    # Deleted solutions
    *(
        path(
            p,
            RedirectView.as_view(
                url=reverse_lazy("storefront:solutions-list")
            ),
        )
        for p in [
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
