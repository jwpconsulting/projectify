"""Workspace models."""
import uuid

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
from ordered_model.models import (
    OrderedModel,
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
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
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
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)


class WorkspaceBoard(TitleDescriptionModel, TimeStampedModel, models.Model):
    """Workspace board."""

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.PROTECT,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)


class WorkspaceBoardSection(
    OrderedModel,
    TitleDescriptionModel,
    TimeStampedModel,
    models.Model,
):
    """Section of a WorkspaceBoard."""

    workspace_board = models.ForeignKey(
        WorkspaceBoard,
        on_delete=models.PROTECT,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    order_with_respect_to = "workspace_board"

    class Meta:
        """Meta."""

        ordering = ("workspace_board", "order")


class Task(
    OrderedModel,
    TitleDescriptionModel,
    TimeStampedModel,
    models.Model,
):
    """Task, belongs to workspace board section."""

    workspace_board_section = models.ForeignKey(
        WorkspaceBoardSection,
        on_delete=models.PROTECT,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    order_with_respect_to = "workspace_board_section"

    class Meta:
        """Meta."""

        ordering = ("workspace_board_section", "order")


class SubTask(
    OrderedModel,
    TitleDescriptionModel,
    TimeStampedModel,
    models.Model,
):
    """SubTask, belongs to Task."""

    task = models.ForeignKey(
        Task,
        on_delete=models.PROTECT,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    order_with_respect_to = "task"

    class Meta:
        """Meta."""

        ordering = ("task", "order")
