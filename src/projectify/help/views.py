# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
"""Help Views."""

import warnings
from pathlib import Path

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from projectify.lib.settings import get_settings
from projectify.lib.utils import markdown_to_safe_html

settings = get_settings()

HELP_TOPICS = {
    "basics": {
        "title": _("Basics"),
        "description": _("Your first steps towards productivity"),
        "markdown_file": Path("basics.md"),
        # These are a bit redundant since "basics" is the key of this entry
        "href": reverse_lazy("help:topic:basics"),
    },
    "workspaces": {
        "title": _("Workspaces"),
        "description": _("Independent spaces at your fingertips"),
        "markdown_file": Path("workspaces.md"),
        "href": reverse_lazy("help:topic:workspaces"),
    },
    "projects": {
        "title": _("Projects"),
        "description": _("Separate projects from each other"),
        "markdown_file": Path("projects.md"),
        "href": reverse_lazy("help:topic:projects"),
    },
    "tasks": {
        "title": _("Tasks"),
        "description": _("All the ins and outs of task creation"),
        "markdown_file": Path("tasks.md"),
        "href": reverse_lazy("help:topic:tasks"),
    },
    "team-members": {
        "title": _("Team members"),
        "description": _("Collaboration starts with an invite"),
        "markdown_file": Path("team-members.md"),
        "href": reverse_lazy("help:topic:team-members"),
    },
    "filters": {
        "title": _("Filters"),
        "description": _("Streamline your workflow with filters"),
        "markdown_file": Path("filters.md"),
        "href": reverse_lazy("help:topic:filters"),
    },
    "billing": {
        "title": _("Billing"),
        "description": _("Billing and payment information"),
        "markdown_file": Path("billing.md"),
        "href": reverse_lazy("help:topic:billing"),
    },
    "trial": {
        "title": _("Trial workspace"),
        "description": _("How to set up a trial workspace"),
        "markdown_file": Path("trial.md"),
        "href": reverse_lazy("help:topic:trial"),
    },
    "quota": {
        "title": _("Workspace quotas"),
        "description": _("Understand workspace resource quotas"),
        "markdown_file": Path("quota.md"),
        "href": reverse_lazy("help:topic:quota"),
    },
    "roles": {
        "title": _("Roles"),
        "description": _("Divide up roles between team members"),
        "markdown_file": Path("roles.md"),
        "href": reverse_lazy("help:topic:roles"),
    },
}

help_topics_with_index = {
    "index": {
        "title": _("Overview"),
        "description": _("Help overview"),
        "markdown_file": Path("overview.md"),
        "href": reverse_lazy("help:list"),
    },
    **HELP_TOPICS,
}


def help_list(request: HttpRequest) -> HttpResponse:
    """Serve Help list page."""
    context = {"helptopics": HELP_TOPICS.values()}
    return render(request, "help/help_list.html", context)


def help_detail(request: HttpRequest, page: str) -> HttpResponse:
    """
    Serve a help detail page for a given topic.

    Because `page` is used to load a markdown file, extra care needs to be
    taken to not let the user load arbitrary files.
    """
    topic = HELP_TOPICS.get(page)
    if topic is None:
        raise Http404(
            _("Couldn't find help for topic {topic}").format(page=page)
        )
    help_text = (
        (settings.BASE_DIR / "help/markdown_en") / topic["markdown_file"]
    ).read_text()

    # NOTE: This is safe as long as we don't let the user control the page
    # (e.g., local file inclusion)
    help_html, toc_html = markdown_to_safe_html(help_text)
    if not toc_html:
        warnings.warn(f"No TOC for help topic {topic}")

    context = {
        "help_html": help_html,
        "toc_html": toc_html,
        "helptopics": help_topics_with_index.values(),
        "helptopic": topic,
    }
    return render(request, "help/help_detail.html", context)
