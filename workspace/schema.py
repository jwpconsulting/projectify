"""Workspace schema."""
import graphene
import graphene_django

from . import (
    models,
)


class Workspace(graphene_django.DjangoObjectType):
    """Workspace."""

    users = graphene.List("user.schema.User")

    def resolve_users(self, info):
        """Resolve workspace users."""
        return self.users.all()

    class Meta:
        """Meta."""

        fields = ("users",)
        model = models.Workspace


class Query:
    """Query."""

    workspaces = graphene.List(Workspace)

    def resolve_workspaces(self, info):
        """Resolve user's workspaces."""
        user = info.context.user
        workspaces = user.workspace_set.all()
        return workspaces
