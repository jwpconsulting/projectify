"""Workspace models."""
import uuid
from datetime import (
    datetime,
)
from typing import (
    TYPE_CHECKING,
    Callable,
    ClassVar,
    Optional,
    cast,
)

from django.conf import (
    settings,
)
from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.db import (
    models,
    transaction,
)
from django.utils.timezone import (
    now,
)
from django.utils.translation import gettext_lazy as _

from django_extensions.db.models import (
    TimeStampedModel,
    TitleDescriptionModel,
)
from typing_extensions import (
    Self,
)

from .const import WorkspaceUserRoles as WorkspaceUserRoles
from .label import (
    Label,
)
from .sub_task import (
    SubTask,
)
from .task import (
    Task,
    TaskQuerySet,
)
from .types import (
    GetOrder,
    SetOrder,
)
from .workspace import Workspace as Workspace
from .workspace import WorkspaceQuerySet as WorkspaceQuerySet
from .workspace_user_invite import (
    WorkspaceUserInvite,
)


# TODO Here we could be using __all__


if TYPE_CHECKING:
    from django.db.models.fields.related import RelatedField  # noqa: F401
    from django.db.models.manager import RelatedManager  # noqa: F401

    from user.models import (  # noqa: F401
        User,
        UserInvite,
    )


Pks = list[str]


class WorkspaceUserQuerySet(models.QuerySet["WorkspaceUser"]):
    """Workspace user queryset."""

    def filter_by_workspace_pks(self, workspace_pks: Pks) -> Self:
        """Filter by workspace pks."""
        return self.filter(workspace__pk__in=workspace_pks)

    def get_by_workspace_and_user(
        self, workspace: Workspace, user: AbstractBaseUser
    ) -> "WorkspaceUser":
        """Get by workspace and user."""
        return self.get(workspace=workspace, user=user)


class WorkspaceUser(TimeStampedModel, models.Model):
    """Workspace to user mapping."""

    workspace = models.ForeignKey["Workspace"](
        Workspace,
        on_delete=models.PROTECT,
    )
    # This defo depends on the User in user/ app
    user = models.ForeignKey["User"](
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    role = models.CharField(
        max_length=10,
        choices=WorkspaceUserRoles.choices,
        default=WorkspaceUserRoles.OBSERVER,
    )
    job_title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    # Sort of nonsensical
    objects: ClassVar[WorkspaceUserQuerySet] = cast(  # type: ignore[assignment]
        WorkspaceUserQuerySet, WorkspaceUserQuerySet.as_manager()
    )

    if TYPE_CHECKING:
        # Related
        user_invite: RelatedField[None, "UserInvite"]

    def assign_role(self, role: str) -> None:
        """
        Assign a new role.

        Saves.
        """
        self.role = role
        self.save()

    class Meta:
        """Meta."""

        unique_together = ("workspace", "user")


class WorkspaceBoardQuerySet(models.QuerySet["WorkspaceBoard"]):
    """WorkspaceBoard Manager."""

    def filter_by_workspace(self, workspace: Workspace) -> Self:
        """Filter by workspace."""
        return self.filter(workspace=workspace)

    def filter_by_user(self, user: AbstractBaseUser) -> Self:
        """Filter by user."""
        return self.filter(workspace__users=user)

    def filter_by_workspace_pks(self, workspace_pks: Pks) -> Self:
        """Filter by workspace pks."""
        return self.filter(workspace__pk__in=workspace_pks)

    def filter_for_user_and_uuid(
        self, user: AbstractBaseUser, uuid: uuid.UUID
    ) -> Self:
        """Get a workspace baord for user and uuid."""
        return self.filter_by_user(user).filter(uuid=uuid)

    def filter_by_archived(self, archived: bool = True) -> Self:
        """Filter by archived boards."""
        return self.filter(archived__isnull=not archived)


class WorkspaceBoard(TitleDescriptionModel, TimeStampedModel, models.Model):
    """Workspace board."""

    workspace = models.ForeignKey["Workspace"](
        Workspace,
        on_delete=models.PROTECT,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    archived = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Archival timestamp of this workspace board."),
    )
    deadline = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Workspace board's deadline"),
    )

    objects: ClassVar[WorkspaceBoardQuerySet] = cast(  # type: ignore[assignment]
        WorkspaceBoardQuerySet, WorkspaceBoardQuerySet.as_manager()
    )

    if TYPE_CHECKING:
        # Related managers
        workspaceboardsection_set: RelatedManager["WorkspaceBoardSection"]

        # For ordering
        get_workspaceboardsection_order: GetOrder
        set_workspaceboardsection_order: SetOrder

    def add_workspace_board_section(
        self, title: str, description: str
    ) -> "WorkspaceBoardSection":
        """Add workspace board section to this workspace board."""
        workspace_board_section: WorkspaceBoardSection = (
            self.workspaceboardsection_set.create(
                title=title,
                description=description,
            )
        )
        return workspace_board_section

    def archive(self) -> None:
        """
        Mark this workspace board as archived.

        Saves model instance.
        """
        self.archived = now()
        self.save()

    def unarchive(self) -> None:
        """
        Mark this workspace board as not archived.

        Saves model instance.
        """
        self.archived = None
        self.save()


class WorkspaceBoardSectionQuerySet(models.QuerySet["WorkspaceBoardSection"]):
    """QuerySet for WorkspaceBoard."""

    def filter_by_workspace_board_pks(self, keys: Pks) -> Self:
        """Filter by workspace boards."""
        return self.filter(workspace_board__pk__in=keys)

    def filter_for_user_and_uuid(
        self, user: AbstractBaseUser, uuid: uuid.UUID
    ) -> Self:
        """Return a workspace for user and uuid."""
        return self.filter(workspace_board__workspace__users=user, uuid=uuid)


class WorkspaceBoardSection(
    TitleDescriptionModel,
    TimeStampedModel,
    models.Model,
):
    """Section of a WorkspaceBoard."""

    workspace_board = models.ForeignKey["WorkspaceBoard"](
        WorkspaceBoard,
        on_delete=models.CASCADE,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    objects: ClassVar[WorkspaceBoardSectionQuerySet] = cast(  # type: ignore[assignment]
        WorkspaceBoardSectionQuerySet,
        WorkspaceBoardSectionQuerySet.as_manager(),
    )

    if TYPE_CHECKING:
        # Related managers
        task_set: RelatedManager["Task"]

        # For ordering
        get_task_order: GetOrder
        set_task_order: SetOrder
        get_next_in_order: Callable[[], "WorkspaceBoardSection"]
        _order: int

    def add_task(
        self, title: str, description: str, deadline: Optional[datetime] = None
    ) -> "Task":
        """Add a task to this section."""
        task: Task = self.task_set.create(
            title=title,
            description=description,
            deadline=deadline,
            workspace=self.workspace_board.workspace,
        )
        return task

    def move_to(self, order: int) -> None:
        """
        Move to specified order n within workspace board.

        No save required.
        """
        neighbor_sections = (
            self.workspace_board.workspaceboardsection_set.select_for_update()
        )
        with transaction.atomic():
            # Force queryset to be evaluated to lock them for the time of
            # this transaction
            len(neighbor_sections)
            current_workspace_board = self.workspace_board
            # Django docs wrong, need to cast to list
            order_list = list(
                current_workspace_board.get_workspaceboardsection_order()
            )
            # The list is ordered by pk, which is not uuid for us
            current_object_index = order_list.index(self.pk)
            # Mutate to perform move operation
            order_list.insert(order, order_list.pop(current_object_index))
            # Set new order
            current_workspace_board.set_workspaceboardsection_order(order_list)
            current_workspace_board.save()

    @property
    def workspace(self) -> Workspace:
        """Get workspace instance."""
        return self.workspace_board.workspace

    class Meta:
        """Meta."""

        order_with_respect_to = "workspace_board"
        constraints = [
            models.UniqueConstraint(
                fields=["workspace_board", "_order"],
                name="unique_workspace_board_order",
                deferrable=models.Deferrable.DEFERRED,
            )
        ]


class TaskLabelQuerySet(models.QuerySet["TaskLabel"]):
    """QuerySet for TaskLabel."""

    def filter_by_task_pks(self, pks: Pks) -> Self:
        """Filter by task pks."""
        return self.filter(task__pk__in=pks)


class TaskLabel(models.Model):
    """A label to task assignment."""

    task = models.ForeignKey["Task"](
        Task,
        on_delete=models.CASCADE,
    )
    label = models.ForeignKey["Label"](
        Label,
        on_delete=models.CASCADE,
    )

    objects: ClassVar[TaskLabelQuerySet] = cast(  # type: ignore[assignment]
        TaskLabelQuerySet, TaskLabelQuerySet.as_manager()
    )

    @property
    def workspace(self) -> Workspace:
        """Get workspace instance."""
        return self.label.workspace

    class Meta:
        """Meta."""

        unique_together = ("task", "label")


class ChatMessageQuerySet(models.QuerySet["ChatMessage"]):
    """ChatMessage query set."""

    def filter_by_task_pks(self, task_pks: Pks) -> Self:
        """Filter by task pks."""
        return self.filter(task__pk__in=task_pks)

    def filter_for_user_and_uuid(
        self, user: AbstractBaseUser, uuid: uuid.UUID
    ) -> Self:
        """Get for a specific workspace user and uuid."""
        kwargs = {
            "task__workspace_board_section__workspace_board__"
            "workspace__users": user,
            "uuid": uuid,
        }
        return self.filter(**kwargs)


class ChatMessage(TimeStampedModel, models.Model):
    """ChatMessage, belongs to Task."""

    task = models.ForeignKey["Task"](
        Task,
        on_delete=models.CASCADE,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    author = models.ForeignKey["WorkspaceUser"](
        WorkspaceUser,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    # XXX
    objects: ClassVar[ChatMessageQuerySet] = cast(  # type: ignore[assignment]
        ChatMessageQuerySet, ChatMessageQuerySet.as_manager()
    )

    @property
    def workspace(self) -> Workspace:
        """Get workspace instance."""
        return self.task.workspace_board_section.workspace_board.workspace

    class Meta:
        """Meta."""

        ordering = ("created",)


__all__ = (
    "Label",
    "SubTask",
    "Task",
    "TaskQuerySet",
    "Workspace",
    "WorkspaceQuerySet",
    "WorkspaceUserInvite",
)
