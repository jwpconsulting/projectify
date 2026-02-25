# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
"""Help urlpatterns."""

from django.urls import include, path

from projectify.help.views import HELP_TOPICS, help_detail, help_list

app_name = "help"

help_page_patterns = tuple(
    path(topic, help_detail, name=topic, kwargs={"page": topic})
    for topic in HELP_TOPICS
)

urlpatterns = (
    path("", help_list, name="list"),
    path("", include((help_page_patterns, "topic"))),
)
