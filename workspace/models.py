"""Workspace models."""
from django.conf import (
    settings,
)
from django.db import (
    models,
)

from django_extensions.db.models import (
    TimeStampedModel,
    TitleDescriptionModel,
)


class WorkspaceManager(models.Manager):
    """Workspace Manager."""

    def get_for_user(self, user):
        """Return workspaces for a user."""
        return user.workspace_set.all()


class Workspace(TitleDescriptionModel, TimeStampedModel, models.Model):
    """Workspace."""

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="WorkspaceUser",
        through_fields=("workspace", "user"),
    )
    objects = WorkspaceManager()


class WorkspaceUser(TimeStampedModel, models.Model):
    """Workspace to user mapping."""

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.PROTECT,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )


class WorkspaceBoard(TitleDescriptionModel, TimeStampedModel, models.Model):
    """Workspace board."""

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.PROTECT,
    )
