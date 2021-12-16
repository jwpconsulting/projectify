"""Workspace admin."""
from django.contrib import (
    admin,
)
from django.utils.translation import gettext_lazy as _

from .models import (
    Workspace,
    WorkspaceBoard,
    WorkspaceBoardSection,
    WorkspaceUser,
)


class WorkspaceUserInline(admin.TabularInline):
    """WorkspaceUser Inline."""

    model = WorkspaceUser
    extra = 0


class WorkspaceBoardInline(admin.TabularInline):
    """WorkspaceBoard Inline."""

    model = WorkspaceBoard
    extra = 0


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    """Workspace Admin."""

    inlines = (WorkspaceUserInline, WorkspaceBoardInline)
    list_display = (
        "title",
        "description",
        "created",
        "modified",
    )


@admin.register(WorkspaceUser)
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


@admin.register(WorkspaceBoard)
class WorkspaceBoardAdmin(admin.ModelAdmin):
    """WorkspaceBoard Admin."""

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


@admin.register(WorkspaceBoardSection)
class WorkspaceBoardSectionAdmin(admin.ModelAdmin):
    """WorkspaceBoardSection Admin."""

    list_display = (
        "title",
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
