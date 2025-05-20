# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
"""Onboading urlpatterns."""

from django.urls import path

from projectify.onboarding.views import about_you, new_workspace, welcome

urlpatterns = [
    path("welcome/", welcome),
    path("about-you/", about_you),
    path("new-workspace/", new_workspace),
]
