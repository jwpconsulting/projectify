"""Workspace admin."""
from django.contrib import (
    admin,
)
from django.utils.translation import gettext_lazy as _

from ordered_model.admin import (
    OrderedModelAdmin,
)

from . import (
    models,
)


class WorkspaceUserInline(admin.TabularInline):
    """WorkspaceUser Inline."""

    model = models.WorkspaceUser
    extra = 0


class WorkspaceBoardInline(admin.TabularInline):
    """WorkspaceBoard Inline."""

    model = models.WorkspaceBoard
    extra = 0


@admin.register(models.Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    """Workspace Admin."""

    inlines = (WorkspaceUserInline, WorkspaceBoardInline)
    list_display = (
        "title",
        "description",
        "created",
        "modified",
    )


@admin.register(models.WorkspaceUser)
class WorkspaceUserAdmin(admin.ModelAdmin):
    """WorkspaceUser Admin."""

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

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance):
        """Return the workspace's title."""
        return instance.workspace.title

    @admin.display(description=_("User email"))
    def user_email(self, instance):
        """Return the workspace's title."""
        return instance.user.email


class WorkspaceBoardSectionInline(admin.TabularInline):
    """WorkspaceBoardSection inline admin."""

    model = models.WorkspaceBoardSection
    extra = 0


@admin.register(models.WorkspaceBoard)
class WorkspaceBoardAdmin(admin.ModelAdmin):
    """WorkspaceBoard Admin."""

    inlines = (WorkspaceBoardSectionInline,)
    list_display = (
        "title",
        "workspace_title",
        "created",
        "modified",
    )
    list_select_related = ("workspace",)

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance):
        """Return the workspace's title."""
        return instance.workspace.title


class TaskInline(admin.TabularInline):
    """Task inline admin."""

    model = models.Task
    extra = 0


@admin.register(models.WorkspaceBoardSection)
class WorkspaceBoardSectionAdmin(OrderedModelAdmin):
    """WorkspaceBoardSection Admin."""

    inlines = (TaskInline,)
    list_display = (
        "title",
        "move_up_down_links",
        "workspace_board_title",
        "workspace_title",
        "created",
        "modified",
    )
    list_select_related = ("workspace_board__workspace",)

    @admin.display(description=_("Workspace board title"))
    def workspace_board_title(self, instance):
        """Return the workspace board's title."""
        return instance.workspace_board.title

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance):
        """Return the workspace's title."""
        return instance.workspace_board.workspace.title


class SubTaskInline(admin.TabularInline):
    """SubTask inline admin."""

    model = models.SubTask
    extra = 0


@admin.register(models.Task)
class TaskAdmin(OrderedModelAdmin):
    """Task Admin."""

    inlines = (SubTaskInline,)
    list_display = (
        "title",
        "move_up_down_links",
        "workspace_board_section_title",
        "workspace_board_title",
        "workspace_title",
        "created",
        "modified",
    )
    list_select_related = (
        "workspace_board_section__workspace_board__workspace",
    )

    @admin.display(description=_("Workspace board section title"))
    def workspace_board_section_title(self, instance):
        """Return the workspace board's title."""
        return instance.workspace_board_section.title

    @admin.display(description=_("Workspace board title"))
    def workspace_board_title(self, instance):
        """Return the workspace board's title."""
        return instance.workspace_board_section.workspace_board.title

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance):
        """Return the workspace's title."""
        return instance.workspace_board_section.workspace_board.workspace.title


@admin.register(models.Label)
class LabelAdmin(admin.ModelAdmin):
    """Label admin."""

    list_display = (
        "name",
        "color",
        "workspace_title",
    )

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance):
        """Return the workspace's title."""
        return instance.workspace.title


@admin.register(models.SubTask)
class SubTaskAdmin(OrderedModelAdmin):
    """SubTask Admin."""

    list_display = (
        "title",
        "move_up_down_links",
        "task_title",
        "workspace_board_section_title",
        "workspace_board_title",
        "workspace_title",
        "created",
        "modified",
    )
    list_select_related = (
        "task__workspace_board_section__workspace_board__workspace",
    )

    @admin.display(description=_("Task title"))
    def task_title(self, instance):
        """Return the task's title."""
        return instance.task.title

    @admin.display(description=_("Workspace board section title"))
    def workspace_board_section_title(self, instance):
        """Return the workspace board's title."""
        return instance.task.workspace_board_section.title

    @admin.display(description=_("Workspace board title"))
    def workspace_board_title(self, instance):
        """Return the workspace board's title."""
        return instance.task.workspace_board_section.workspace_board.title

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance):
        """Return the workspace's title."""
        workspace_board = instance.task.workspace_board_section.workspace_board
        return workspace_board.workspace.title
