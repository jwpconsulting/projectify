# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
"""Storefront urlpatterns."""

from django.urls import include, path

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

solution_patterns = [
    path("", solutions_index, name="list"),
    path("development-teams", solutions_development_teams, name="development_teams"),
    path("project-management", solutions_project_management, name="project_management"),
    path("academic", solutions_academic, name="academic"),
]

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
    path("solutions/", include((solution_patterns, "solutions"))),
    path("", index, name="landing"),
]
