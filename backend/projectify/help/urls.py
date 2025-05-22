# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
"""Help urlpatterns."""

from django.urls import path

from projectify.help.views import help_detail, help_list

app_name = "help"

urlpatterns = [
    path("help/", help_list, name="list"),
    # TODO: Add safe urls for help detail pages
    path("help/<slug:page>/", help_detail, name="detail"),
]
