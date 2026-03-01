# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2022, 2023 JWP Consulting GK
"""Workspace admin."""

from typing import Optional

from django.contrib import admin
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _

from .models import (
    ChatMessage,
    Label,
    Project,
    Section,
    Task,
    TaskLabel,
    TeamMember,
    TeamMemberInvite,
    Workspace,
)


class TeamMemberInline(admin.TabularInline[TeamMember]):
    """TeamMember Inline."""

    model = TeamMember
    extra = 0


class ProjectInline(admin.TabularInline[Project]):
    """Project Inline."""

    model = Project
    extra = 0


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin[Workspace]):
    """Workspace Admin."""

    inlines = (TeamMemberInline, ProjectInline)
    list_display = (
        "title",
        "description",
        "created",
        "modified",
    )
    readonly_fields = ("uuid",)
    search_fields = ("title",)
    search_help_text = _("You can search by workspace title")


@admin.register(TeamMemberInvite)
class TeamMemberInviteAdmin(admin.ModelAdmin[TeamMemberInvite]):
    """Team member invite admin."""

    list_display = ("workspace_title", "redeemed", "redeemed_when")
    list_select_related = ("workspace",)
    list_filter = (
        "redeemed",
        "redeemed_when",
    )

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: TeamMemberInvite) -> str:
        """Return the workspace's title."""
        return instance.workspace.title

    def has_change_permission(
        self, request: HttpRequest, obj: Optional[TeamMemberInvite] = None
    ) -> bool:
        """Forbid anyone from changing this."""
        del request
        del obj
        return False


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin[TeamMember]):
    """TeamMember Admin."""

    list_display = (
        "workspace_title",
        "user_email",
        "created",
        "modified",
        "role",
    )
    list_filter = ("role",)
    list_select_related = (
        "workspace",
        "user",
    )
    search_fields = (
        "workspace__title",
        "user__email",
        "user__preferred_name",
    )
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


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin[Project]):
    """Project Admin."""

    inlines = (SectionInline,)
    list_display = (
        "title",
        "workspace_title",
        "created",
        "modified",
    )
    list_select_related = ("workspace",)
    readonly_fields = ("uuid",)
    search_fields = (
        "title",
        "workspace__title",
        "uuid",
    )

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: Project) -> str:
        """Return the workspace's title."""
        return instance.workspace.title


class TaskInline(admin.TabularInline[Task]):
    """Task inline admin."""

    model = Task
    extra = 0
    readonly_fields = ("assignee",)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin[Section]):
    """Section Admin."""

    inlines = (TaskInline,)
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


class TaskLabelInline(admin.TabularInline[TaskLabel]):
    """TaskLabel inline admin."""

    model = TaskLabel
    extra = 0


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin[Task]):
    """Task Admin."""

    inlines = (TaskLabelInline,)
    list_display = (
        "title",
        "section_title",
        "project_title",
        "workspace_title",
        "created",
        "modified",
    )
    list_select_related = ("section__project__workspace",)
    readonly_fields = ("uuid", "assignee")

    @admin.display(description=_("Section title"))
    def section_title(self, instance: Task) -> str:
        """Return the project's title."""
        return instance.section.title

    @admin.display(description=_("Project title"))
    def project_title(self, instance: Task) -> str:
        """Return the project's title."""
        return instance.section.project.title

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: Task) -> str:
        """Return the workspace's title."""
        return instance.section.project.workspace.title


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin[Label]):
    """Label admin."""

    list_display = (
        "name",
        "color",
        "workspace_title",
    )
    list_select_related = ("workspace",)
    readonly_fields = ("uuid",)

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: Label) -> str:
        """Return the workspace's title."""
        return instance.workspace.title


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin[ChatMessage]):
    """ChatMessage admin."""

    list_display = (
        "task_title",
        "section_title",
        "project_title",
        "workspace_title",
        "created",
        "modified",
    )
    list_select_related = ("task__section__project__workspace",)
    readonly_fields = ("uuid", "author")

    @admin.display(description=_("Task title"))
    def task_title(self, instance: ChatMessage) -> str:
        """Return the task's title."""
        return instance.task.title

    @admin.display(description=_("Section title"))
    def section_title(self, instance: ChatMessage) -> str:
        """Return the project's title."""
        return instance.task.section.title

    @admin.display(description=_("Project title"))
    def project_title(self, instance: ChatMessage) -> str:
        """Return the project's title."""
        return instance.task.section.project.title

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: ChatMessage) -> str:
        """Return the workspace's title."""
        project = instance.task.section.project
        return project.workspace.title
