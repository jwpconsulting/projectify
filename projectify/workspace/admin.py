# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021-2024,2026 JWP Consulting GK
"""Workspace admin."""

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from projectify.lib.admin import ReadOnlyAdmin

from .models import Project, Task, TeamMember, TeamMemberInvite, Workspace


class ProjectInline(admin.TabularInline[Project]):
    """Project Inline."""

    model = Project
    extra = 0
    fields = ("archived",)
    show_change_link = True
    view_on_site = False


class TeamMemberInline(admin.TabularInline[TeamMember]):
    """TeamMember Inline."""

    model = TeamMember
    extra = 0
    fields = ("role", "job_title")

    def get_queryset(self, request: HttpRequest) -> QuerySet[TeamMember]:
        """Select related user_invite and user."""
        return super().get_queryset(request).select_related("user")

    # https://docs.djangoproject.com/en/6.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.view_on_site
    def view_on_site(self, obj: TeamMember) -> str:
        """Return a link to the user's admin change page."""
        return reverse("admin:user_user_change", args=[obj.user.pk])


class TeamMemberInviteInline(
    ReadOnlyAdmin[TeamMemberInvite], admin.TabularInline[TeamMemberInvite]
):
    """Team member invite inline."""

    model = TeamMemberInvite
    readonly_fields = ("redeemed_when",)
    fields = ("user_invite", "redeemed", "redeemed_when")

    def get_queryset(self, request: HttpRequest) -> QuerySet[TeamMemberInvite]:
        """Select related user_invite and user."""
        return (
            super()
            .get_queryset(request)
            .select_related("user_invite", "user_invite__user")
        )


@admin.register(Workspace)
class WorkspaceAdmin(ReadOnlyAdmin[Workspace], admin.ModelAdmin[Workspace]):
    """Workspace Admin."""

    inlines = (ProjectInline, TeamMemberInline, TeamMemberInviteInline)
    list_display = ("title", "description", "created", "modified")
    readonly_fields = ("uuid",)
    search_fields = ("title",)
    search_help_text = _("You can search by workspace title")


class TaskInline(admin.TabularInline[Task]):
    """Task inline admin."""

    model = Task
    extra = 0
    readonly_fields = ("assignee",)
    fields = ("due_date", "done", "assignee")
    view_on_site = False

    def get_queryset(self, request: HttpRequest) -> QuerySet[Task]:
        """Select related user_invite and user."""
        return (
            super()
            .get_queryset(request)
            .select_related("assignee", "assignee__user")
        )


@admin.register(Project)
class ProjectAdmin(ReadOnlyAdmin[Project], admin.ModelAdmin[Project]):
    """Project Admin."""

    inlines = (TaskInline,)
    list_display = ("title", "workspace_title", "created", "modified")
    list_select_related = ("workspace",)
    readonly_fields = ("uuid",)
    search_fields = ("title", "workspace__title", "uuid")

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: Project) -> str:
        """Return the workspace's title."""
        return instance.workspace.title
