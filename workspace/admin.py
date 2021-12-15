"""Workspace admin."""
from django.contrib import (
    admin,
)

from .models import (
    Workspace,
    WorkspaceUser,
)


class WorkspaceUserInline(admin.TabularInline):
    """WorkspaceUser Inline."""

    model = WorkspaceUser
    extra = 0


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    """Workspace Admin."""

    inlines = (WorkspaceUserInline,)


@admin.register(WorkspaceUser)
class WorkspaceUserAdmin(admin.ModelAdmin):
    """WorkspaceUser Admin."""
