# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2021, 2022, 2023 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Workspace admin."""
from django.contrib import (
    admin,
)
from django.utils.translation import gettext_lazy as _

from . import (
    models,
)


class TeamMemberInline(admin.TabularInline[models.TeamMember]):
    """TeamMember Inline."""

    model = models.TeamMember
    extra = 0


class ProjectInline(admin.TabularInline[models.Project]):
    """Project Inline."""

    model = models.Project
    extra = 0


@admin.register(models.Workspace)
class WorkspaceAdmin(admin.ModelAdmin[models.Workspace]):
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


@admin.register(models.TeamMemberInvite)
class TeamMemberInviteAdmin(admin.ModelAdmin[models.TeamMemberInvite]):
    """Team member invite admin."""

    list_display = ("workspace_title",)
    list_select_related = ("workspace",)

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: models.TeamMemberInvite) -> str:
        """Return the workspace's title."""
        return instance.workspace.title


@admin.register(models.TeamMember)
class TeamMemberAdmin(admin.ModelAdmin[models.TeamMember]):
    """TeamMember Admin."""

    list_display = (
        "workspace_title",
        "user_email",
        "created",
        "modified",
    )
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
    def workspace_title(self, instance: models.TeamMember) -> str:
        """Return the workspace's title."""
        return instance.workspace.title

    @admin.display(description=_("User email"))
    def user_email(self, instance: models.TeamMember) -> str:
        """Return the workspace's title."""
        return instance.user.email


class SectionInline(admin.TabularInline[models.Section]):
    """Section inline admin."""

    model = models.Section
    extra = 0


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin[models.Project]):
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

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: models.Project) -> str:
        """Return the workspace's title."""
        return instance.workspace.title


class TaskInline(admin.TabularInline[models.Task]):
    """Task inline admin."""

    model = models.Task
    extra = 0
    readonly_fields = ("assignee",)


@admin.register(models.Section)
class SectionAdmin(admin.ModelAdmin[models.Section]):
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
    def project_title(self, instance: models.Section) -> str:
        """Return the project's title."""
        return instance.project.title

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: models.Section) -> str:
        """Return the workspace's title."""
        return instance.project.workspace.title


class SubTaskInline(admin.TabularInline[models.SubTask]):
    """SubTask inline admin."""

    model = models.SubTask
    extra = 0


class TaskLabelInline(admin.TabularInline[models.TaskLabel]):
    """TaskLabel inline admin."""

    model = models.TaskLabel
    extra = 0


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin[models.Task]):
    """Task Admin."""

    inlines = (SubTaskInline, TaskLabelInline)
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
    def section_title(self, instance: models.Task) -> str:
        """Return the project's title."""
        return instance.section.title

    @admin.display(description=_("Project title"))
    def project_title(self, instance: models.Task) -> str:
        """Return the project's title."""
        return instance.section.project.title

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: models.Task) -> str:
        """Return the workspace's title."""
        return instance.section.project.workspace.title


@admin.register(models.Label)
class LabelAdmin(admin.ModelAdmin[models.Label]):
    """Label admin."""

    list_display = (
        "name",
        "color",
        "workspace_title",
    )
    list_select_related = ("workspace",)
    readonly_fields = ("uuid",)

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: models.Label) -> str:
        """Return the workspace's title."""
        return instance.workspace.title


@admin.register(models.SubTask)
class SubTaskAdmin(admin.ModelAdmin[models.SubTask]):
    """SubTask Admin."""

    list_display = (
        "title",
        "task_title",
        "section_title",
        "project_title",
        "workspace_title",
        "created",
        "modified",
    )
    list_select_related = ("task__section__project__workspace",)
    readonly_fields = ("uuid",)

    @admin.display(description=_("Task title"))
    def task_title(self, instance: models.SubTask) -> str:
        """Return the task's title."""
        return instance.task.title

    @admin.display(description=_("Section title"))
    def section_title(self, instance: models.SubTask) -> str:
        """Return the project's title."""
        return instance.task.section.title

    @admin.display(description=_("Project title"))
    def project_title(self, instance: models.SubTask) -> str:
        """Return the project's title."""
        return instance.task.section.project.title

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: models.SubTask) -> str:
        """Return the workspace's title."""
        project = instance.task.section.project
        return project.workspace.title


@admin.register(models.ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin[models.ChatMessage]):
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
    def task_title(self, instance: models.ChatMessage) -> str:
        """Return the task's title."""
        return instance.task.title

    @admin.display(description=_("Section title"))
    def section_title(self, instance: models.ChatMessage) -> str:
        """Return the project's title."""
        return instance.task.section.title

    @admin.display(description=_("Project title"))
    def project_title(self, instance: models.ChatMessage) -> str:
        """Return the project's title."""
        return instance.task.section.project.title

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: models.ChatMessage) -> str:
        """Return the workspace's title."""
        project = instance.task.section.project
        return project.workspace.title
