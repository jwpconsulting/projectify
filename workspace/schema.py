"""Workspace schema."""
import graphene
import graphene_django

from . import (
    models,
)


class Workspace(graphene_django.DjangoObjectType):
    """Workspace."""

    users = graphene.List("user.schema.User")
    workspace_boards = graphene.List("workspace.schema.WorkspaceBoard")

    def resolve_users(self, info):
        """Resolve workspace users."""
        return self.users.all()

    def resolve_workspace_boards(self, info):
        """Resolve workspace baords."""
        return self.workspaceboard_set.all()

    class Meta:
        """Meta."""

        fields = ("users", "created", "modified")
        model = models.Workspace


class WorkspaceBoard(graphene_django.DjangoObjectType):
    """WorkspaceBoard."""

    class Meta:
        """Meta."""

        fields = ("created", "modified")
        model = models.WorkspaceBoard


class Query:
    """Query."""

    workspaces = graphene.List(Workspace)

    def resolve_workspaces(self, info):
        """Resolve user's workspaces."""
        user = info.context.user
        workspaces = user.workspace_set.all()
        return workspaces
