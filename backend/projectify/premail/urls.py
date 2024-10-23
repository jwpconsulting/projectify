# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2023 JWP Consulting GK
"""Premail urlpatterns."""

from django.urls import (
    path,
)

from .views import (
    EmailList,
    EmailPreview,
)

app_name = "premail"


urlpatterns = (
    path(r"", EmailList.as_view(), name="email-list"),
    path(
        r"<slug:slug>",
        EmailPreview.as_view(),
        name="email-preview",
    ),
)
