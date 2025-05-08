# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
"""Help urlpatterns."""

from django.urls import path

from projectify.help.views import help_list

urlpatterns = [
    path("help/", help_list),
]
