# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
"""Help urlpatterns."""

from django.urls import include, path, reverse_lazy
from django.views.generic import RedirectView

from projectify.help.views import HELP_TOPICS, help_detail, help_list

app_name = "help"

help_page_patterns = tuple(
    path(topic, help_detail, name=topic, kwargs={"page": topic})
    for topic in HELP_TOPICS
)

urlpatterns = (
    path("help", help_list, name="list"),
    path("help/", RedirectView.as_view(url=reverse_lazy("help:list"))),
    path("help/", include((help_page_patterns, "topic"))),
)
