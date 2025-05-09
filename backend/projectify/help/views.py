# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
"""Help Views."""

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def get_help_topics(include_overview: bool):
    """Return a list of help topics."""
    return [
        *(
            [
                {
                    "title": "Overview",
                    "description": "",
                    "href": "/help",
                }
            ]
            if include_overview
            else []
        ),
        {
            "title": "Basics",
            "description": "Your first steps towards productivity",
            "href": "/help/basics/",
        },
        {
            "title": "Workspaces",
            "description": "Independent spaces at your fingertips",
            "href": "/help/workspaces/",
        },
        {
            "title": "Projects",
            "description": "Separate projects from each other",
            "href": "/help/projects/",
        },
        {
            "title": "Sections",
            "description": "Maximize the efficiency of your tasks",
            "href": "/help/sections/",
        },
        {
            "title": "Tasks",
            "description": "All the ins and outs of task creation",
            "href": "/help/tasks/",
        },
        {
            "title": "Labels",
            "description": "Create categories for your tasks",
            "href": "/help/labels/",
        },
        {
            "title": "Team members",
            "description": "Collaboration starts with an invite",
            "href": "/help/team-members/",
        },
        {
            "title": "Filters",
            "description": "Streamline your workflow with filters",
            "href": "/help/filters/",
        },
        {
            "title": "Billing",
            "description": "Billing and payment information",
            "href": "/help/billing/",
        },
        {
            "title": "Trial workspace",
            "description": "How to set up a trial workspace",
            "href": "/help/trial/",
        },
        {
            "title": "Workspace quotas",
            "description": "Understand workspace resource quotas",
            "href": "/help/quota/",
        },
        {
            "title": "Roles",
            "description": "Divide up roles between team members",
            "href": "/help/roles/",
        },
        {
            "title": "Keyboard shortcuts",
            "description": "Use keyboard shortcuts to improve productivity",
            "href": "/help/keyboard-shortcuts/",
        },
    ]


def help_list(request: HttpRequest) -> HttpResponse:
    """Serve Help list page."""
    context = {"helptopics": get_help_topics(False)}
    return render(request, "help/help_list.html", context)


def help_detail(request: HttpRequest, page: str) -> HttpResponse:
    """Serve Help list page."""
    help_page = (
        settings.BASE_DIR.parent.parent
        / "frontend/src/messages/en/help/page.md"
    ).with_stem(page)
    markdowntext = help_page.read_text()
    helptopics = get_help_topics(True)
    helptopic = [
        topic for topic in helptopics if topic["href"] == request.path
    ]
    context = {
        "help_text": markdowntext,
        "helptopics": helptopics,
        "helptopic": helptopic[0],
    }
    return render(request, "help/help_detail.html", context)
