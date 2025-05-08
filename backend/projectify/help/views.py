# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
"""Help Views."""


from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def help_list(request: HttpRequest) -> HttpResponse:
    """Serve Help list page."""
    helptopics = [
        # {
        #   "title": "Overview",
        #   "description": "",
        #   "href": "/help",
        #   "isOverview": True,
        # },
        {
            "title": "Basics",
            "description": "Your first steps towards productivity",
            "href": "help/basics/",
        },
        {
            "title": "Workspaces",
            "description": "Independent spaces at your fingertips",
            "href": "/help/workspaces",
        },
        {
            "title": "Projects",
            "description": "Separate projects from each other",
            "href": "/help/projects",
        },
        {
            "title": "Sections",
            "description": "Maximize the efficiency of your tasks",
            "href": "/help/sections",
        },
        {
            "title": "Tasks",
            "description": "All the ins and outs of task creation",
            "href": "/help/tasks",
        },
        {
            "title": "Labels",
            "description": "Create categories for your tasks",
            "href": "/help/labels",
        },
        {
            "title": "Team members",
            "description": "Collaboration starts with an invite",
            "href": "/help/team-members",
        },
        {
            "title": "Filters",
            "description": "Streamline your workflow with filters",
            "href": "/help/filters",
        },
        {
            "title": "Billing",
            "description": "Billing and payment information",
            "href": "/help/billing",
        },
        {
            "title": "Trial workspace",
            "description": "How to set up a trial workspace",
            "href": "/help/trial",
        },
        {
            "title": "Workspace quotas",
            "description": "Understand workspace resource quotas",
            "href": "/help/quota",
        },
        {
            "title": "Roles",
            "description": "Divide up roles between team members",
            "href": "/help/roles",
        },
        {
            "title": "Keyboard shortcuts",
            "description": "Use keyboard shortcuts to improve productivity",
            "href": "/help/keyboard-shortcuts",
        },
    ]
    context = {"helptopics": helptopics}
    return render(request, "help/help_list.html", context)
