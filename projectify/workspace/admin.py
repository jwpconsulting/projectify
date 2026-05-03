# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021-2024,2026 JWP Consulting GK
"""Workspace admin."""

from typing import Optional, TypeVar

from django.contrib import admin
from django.db.models import Model
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _

from .models import (
    Project,
    Section,
    Task,
    TeamMember,
    TeamMemberInvite,
    Workspace,
)

M = TypeVar("M", bound=Model)


class ReadOnlyAdmin[M]:
    """Admin Mixin that forbids anyone from making changes to this model."""

    def has_add_permission(
        self, request: HttpRequest, obj: Optional[M] = None
    ) -> bool:
        """Forbid anyone from adding objects."""
        del request
        del obj
        return False

    def has_change_permission(
        self, request: HttpRequest, obj: Optional[M] = None
    ) -> bool:
        """Forbid anyone from changing objects."""
        del request
        del obj
        return False


class TeamMemberInline(admin.TabularInline[TeamMember]):
    """TeamMember Inline."""

    model = TeamMember
    extra = 0


class ProjectInline(admin.TabularInline[Project]):
    """Project Inline."""

    model = Project
    extra = 0


@admin.register(Workspace)
class WorkspaceAdmin(ReadOnlyAdmin[Workspace], admin.ModelAdmin[Workspace]):
    """Workspace Admin."""

    inlines = (TeamMemberInline, ProjectInline)
    list_display = ("title", "description", "created", "modified")
    readonly_fields = ("uuid",)
    search_fields = ("title",)
    search_help_text = _("You can search by workspace title")


@admin.register(TeamMemberInvite)
class TeamMemberInviteAdmin(
    ReadOnlyAdmin[TeamMemberInvite], admin.ModelAdmin[TeamMemberInvite]
):
    """Team member invite admin."""

    list_display = ("workspace_title", "redeemed", "redeemed_when")
    list_select_related = ("workspace",)
    list_filter = ("redeemed", "redeemed_when")

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: TeamMemberInvite) -> str:
        """Return the workspace's title."""
        return instance.workspace.title


@admin.register(TeamMember)
class TeamMemberAdmin(ReadOnlyAdmin[TeamMember], admin.ModelAdmin[TeamMember]):
    """TeamMember Admin."""

    list_display = (
        "workspace_title",
        "user_email",
        "created",
        "modified",
        "role",
    )
    list_filter = ("role",)
    list_select_related = ("workspace", "user")
    search_fields = ("workspace__title", "user__email", "user__preferred_name")
    search_help_text = _(
        "You can seach by workspace title, user email and preferred name"
    )

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: TeamMember) -> str:
        """Return the workspace's title."""
        return instance.workspace.title

    @admin.display(description=_("User email"))
    def user_email(self, instance: TeamMember) -> str:
        """Return the workspace's title."""
        return instance.user.email


class SectionInline(admin.TabularInline[Section]):
    """Section inline admin."""

    model = Section
    extra = 0


class TaskInline(admin.TabularInline[Task]):
    """Task inline admin."""

    model = Task
    extra = 0
    readonly_fields = ("assignee",)


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


@admin.register(Section)
class SectionAdmin(ReadOnlyAdmin[Section], admin.ModelAdmin[Section]):
    """Section Admin."""

    list_display = (
        "title",
        "project_title",
        "workspace_title",
        "created",
        "modified",
    )
    list_select_related = ("project__workspace",)
    readonly_fields = ("uuid",)

    @admin.display(description=_("Project title"))
    def project_title(self, instance: Section) -> str:
        """Return the project's title."""
        return instance.project.title

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: Section) -> str:
        """Return the workspace's title."""
        return instance.project.workspace.title


@admin.register(Task)
class TaskAdmin(ReadOnlyAdmin[Task], admin.ModelAdmin[Task]):
    """Task Admin."""

    list_display = (
        "title",
        "project_title",
        "workspace_title",
        "created",
        "modified",
    )
    list_select_related = ("project__workspace",)
    readonly_fields = ("uuid", "assignee")

    @admin.display(description=_("Project title"))
    def project_title(self, instance: Task) -> str:
        """Return the project's title."""
        return str(instance.project.title)

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: Task) -> str:
        """Return the workspace's title."""
        return str(instance.project.workspace.title)
