"""Workspace models."""
import uuid

from django.conf import (
    settings,
)
from django.db import (
    models,
    transaction,
)

from django_extensions.db.models import (
    TimeStampedModel,
    TitleDescriptionModel,
)
from ordered_model.models import (
    OrderedModel,
    OrderedModelManager,
)


class WorkspaceManager(models.Manager):
    """Workspace Manager."""

    def get_for_user(self, user):
        """Return workspaces for a user."""
        return user.workspace_set.all()

    def get_for_user_and_uuid(self, user, uuid):
        """Return workspace for user and uuid."""
        return user.workspace_set.get(uuid=uuid)


class Workspace(TitleDescriptionModel, TimeStampedModel, models.Model):
    """Workspace."""

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="WorkspaceUser",
        through_fields=("workspace", "user"),
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    objects = WorkspaceManager()

    def add_workspace_board(self, title, description):
        """Add workspace board."""
        return self.workspaceboard_set.create(
            title=title,
            description=description,
        )


class WorkspaceUserQuerySet(models.QuerySet):
    """Workspace user queryset."""

    def filter_by_workspace_pks(self, workspace_pks):
        """Filter by workspace pks."""
        return self.filter(workspace__pk__in=workspace_pks)


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

    objects = WorkspaceUserQuerySet.as_manager()


class WorkspaceBoardManager(models.Manager):
    """WorkspaceBoard Manager."""

    def filter_by_workspace_pks(self, workspace_pks):
        """Filter by workspace pks."""
        return self.filter(workspace__pk__in=workspace_pks)

    def get_for_user_and_uuid(self, user, uuid):
        """Get a workspace baord for user and uuid."""
        return self.filter(workspace__users=user).get(uuid=uuid)


class WorkspaceBoard(TitleDescriptionModel, TimeStampedModel, models.Model):
    """Workspace board."""

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.PROTECT,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    objects = WorkspaceBoardManager()

    def add_workspace_board_section(self, title, description):
        """Add workspace board section to this workspace board."""
        return self.workspaceboardsection_set.create(
            title=title,
            description=description,
        )


class WorkspaceBoardSectionManager(OrderedModelManager):
    """Manager for WorkspaceBoard."""

    def filter_by_workspace_board_pks(self, keys):
        """Filter by workspace boards."""
        return self.filter(workspace_board__pk__in=keys)

    def get_for_user_and_uuid(self, user, uuid):
        """Return a workspace for user and uuid."""
        return self.filter(workspace_board__workspace__users=user,).get(
            uuid=uuid,
        )


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
    objects = WorkspaceBoardSectionManager()
    order_with_respect_to = "workspace_board"

    def add_task(self, title, description):
        """Add a task to this section."""
        return self.task_set.create(title=title, description=description)

    class Meta:
        """Meta."""

        ordering = ("workspace_board", "order")


class TaskManager(OrderedModelManager):
    """Manager for Task."""

    def filter_by_workspace_board_section_pks(
        self,
        workspace_board_section_pks,
    ):
        """Filter by workspace board section pks."""
        return self.filter(
            workspace_board_section__pk__in=workspace_board_section_pks,
        )

    def get_for_user_and_uuid(self, user, uuid):
        """Return task from user workspace corresponding to uuid."""
        return self.filter(
            workspace_board_section__workspace_board__workspace__users=user,
        ).get(uuid=uuid)


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

    objects = TaskManager()

    order_with_respect_to = "workspace_board_section"

    def move_to(self, workspace_board_section, position):
        """
        Move to specified workspace board section and to position n.

        No save required.
        """
        neighbor_tasks = (
            self.workspace_board_section.task_set.select_for_update()
        )
        other_tasks = workspace_board_section.task_set.select_for_update()
        with transaction.atomic():
            # Force both querysets to be evaluated to lock them for the time of
            # this transaction
            list(neighbor_tasks)
            list(other_tasks)
            self.workspace_board_section = workspace_board_section
            self.save()
            # XXX hack
            qs = self.get_ordering_queryset()
            if len(qs) == 1:
                # If there is nothing to order, move along
                self.order = 0
                self.save()
                return
            bottom_plus_one = qs.get_next_order()
            self.to(bottom_plus_one)
            self.to(position)

    def add_sub_task(self, title, description):
        """Add a sub task."""
        return self.subtask_set.create(title=title, description=description)

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
