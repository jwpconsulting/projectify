"""Workspace models."""
import uuid
from datetime import (
    datetime,
)
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Iterable,
    Optional,
    Sequence,
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

import pgtrigger
from django_extensions.db.models import (
    TimeStampedModel,
    TitleDescriptionModel,
)
from typing_extensions import (
    Self,
)
from user import models as user_models

from . import (
    signal_defs,
)


if TYPE_CHECKING:
    from django.db.models.fields.related import RelatedField  # noqa: F401
    from django.db.models.manager import RelatedManager  # noqa: F401

    from corporate.models import Customer  # noqa: F401
    from user.models import (  # noqa: F401
        User,
        UserInvite,
    )


Pks = list[str]

GetOrder = Callable[[], Iterable[int]]
SetOrder = Callable[[Sequence[int]], None]


class WorkspaceQuerySet(models.QuerySet["Workspace"]):
    """Workspace Manager."""

    def get_for_user(self, user: AbstractBaseUser) -> Self:
        """Return workspaces for a user."""
        return self.filter(users=user)

    def filter_for_user_and_uuid(
        self, user: AbstractBaseUser, uuid: uuid.UUID
    ) -> Self:
        """Return workspace for user and uuid."""
        return self.get_for_user(user).filter(uuid=uuid)


@pgtrigger.register(
    pgtrigger.Trigger(
        name="ensure_correct_highest_task_number",
        when=pgtrigger.Before,
        operation=pgtrigger.Update,
        func="""
              DECLARE
                max_task_number   INTEGER;
              BEGIN
                SELECT MAX(workspace_task.number) INTO max_task_number
                FROM workspace_task
                WHERE workspace_task.workspace_id = NEW.id;
                IF NEW.highest_task_number < max_task_number THEN
                    RAISE EXCEPTION 'invalid highest_task_number:  \
                    highest_task_number cannot be lower than a task number.';
                END IF;
                RETURN NEW;
              END;""",
    )
)
class Workspace(TitleDescriptionModel, TimeStampedModel, models.Model):
    """Workspace."""

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="WorkspaceUser",
        through_fields=("workspace", "user"),
    )  # type: models.ManyToManyField[AbstractBaseUser, "WorkspaceUser"]
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(
        upload_to="workspace_picture/",
        blank=True,
        null=True,
    )

    highest_task_number = models.IntegerField(default=0)

    objects = cast(WorkspaceQuerySet, WorkspaceQuerySet.as_manager())

    if TYPE_CHECKING:
        # Related fields
        customer: RelatedField[None, "Customer"]

        # Related sets
        workspaceboard_set: RelatedManager["WorkspaceBoard"]
        workspaceuser_set: RelatedManager["WorkspaceUser"]
        workspaceuserinvite_set: RelatedManager["WorkspaceUserInvite"]
        label_set: RelatedManager["Label"]

    def add_workspace_board(
        self, title: str, description: str, deadline: Optional[datetime] = None
    ) -> "WorkspaceBoard":
        """Add workspace board."""
        workspace_board: WorkspaceBoard = self.workspaceboard_set.create(
            title=title,
            description=description,
            deadline=deadline,
        )
        return workspace_board

    def add_user(self, user: AbstractBaseUser) -> AbstractBaseUser:
        """
        Add user to workspace.

        Return user.
        """
        self.workspaceuser_set.create(user=user)
        return user

    @transaction.atomic
    def remove_user(self, user: "User") -> "User":
        """
        Remove user from workspace.

        Removes the user from task assignments.

        Return user.
        """
        workspace_user = self.workspaceuser_set.get(user=user)
        workspace_user.delete()
        return user

    @transaction.atomic
    def invite_user(self, email: str) -> "WorkspaceUserInvite":
        """Invite a user to this workspace."""
        invite_check_qs = WorkspaceUserInvite.objects.filter(
            user_invite__email=email,
            workspace=self,
        )
        if invite_check_qs.exists():
            raise ValueError(_("Email is already invited"))
        already_user_qs = self.users.filter(
            email=email,
        )
        if already_user_qs.exists():
            raise ValueError(_("Email is already workspace user"))
        user_invite = user_models.UserInvite.objects.invite_user(email)
        workspace_user_invite: WorkspaceUserInvite = (
            self.workspaceuserinvite_set.create(
                user_invite=user_invite,
                workspace=self,
            )
        )
        signal_defs.workspace_user_invited.send(
            sender=self.__class__,
            instance=workspace_user_invite,
        )
        return workspace_user_invite

    @transaction.atomic
    def uninvite_user(self, email: str) -> None:
        """Remove a users invitation."""
        workspace_user_invite = self.workspaceuserinvite_set.get(
            user_invite__email=email,
        )
        workspace_user_invite.delete()

    @transaction.atomic
    def increment_highest_task_number(self) -> int:
        """
        Increment and return highest task number.

        Atomic.
        """
        qs = Workspace.objects.filter(pk=self.pk).select_for_update()
        qs.update(highest_task_number=models.F("highest_task_number") + 1)
        return qs.get().highest_task_number

    def has_at_least_role(
        self, workspace_user: "WorkspaceUser", role: str
    ) -> bool:
        """Check if a workspace user has at least a given role."""
        if not workspace_user.workspace == self:
            return False
        if role == WorkspaceUserRoles.OBSERVER:
            return workspace_user.role in OBSERVER_EQUIVALENT
        elif role == WorkspaceUserRoles.MEMBER:
            return workspace_user.role in MEMBER_EQUIVALENT
        elif role == WorkspaceUserRoles.MAINTAINER:
            return workspace_user.role in MAINTAINER_EQUIVALENT
        elif role == WorkspaceUserRoles.OWNER:
            return workspace_user.role in OWNER_EQUIVALENT
        else:
            raise ValueError(
                f"This just happened: {workspace_user} {role} {self}"
            )

    @property
    def workspace(self) -> Self:
        """Get workspace instance."""
        return self


class WorkspaceUserInviteQuerySet(models.QuerySet["WorkspaceUserInvite"]):
    """QuerySet for WorkspaceUserInvite."""

    def filter_by_workspace_pks(self, workspace_pks: Pks) -> Self:
        """Filter by workspace pks."""
        return self.filter(workspace__pk__in=workspace_pks)

    def filter_by_redeemed(self, redeemed: bool = True) -> Self:
        """Filter by redeemed workspace user invites."""
        return self.filter(redeemed=redeemed)


class WorkspaceUserInvite(TimeStampedModel, models.Model):
    """UserInvites belonging to this workspace."""

    user_invite = models.ForeignKey["UserInvite"](
        "user.UserInvite",
        on_delete=models.CASCADE,
    )
    workspace = models.ForeignKey["Workspace"](
        Workspace,
        on_delete=models.CASCADE,
    )
    redeemed = models.BooleanField(
        default=False,
        help_text=_("Has this invite been redeemed?"),
    )

    objects = cast(
        WorkspaceUserInviteQuerySet, WorkspaceUserInviteQuerySet.as_manager()
    )

    def redeem(self) -> None:
        """
        Redeem invite.

        Save.
        """
        assert not self.redeemed
        self.redeemed = True
        self.save()

    class Meta:
        """Meta."""

        unique_together = ("user_invite", "workspace")


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


class WorkspaceUserRoles(models.TextChoices):
    """Roles available."""

    OBSERVER = "OBSERVER", _("Observer")
    MEMBER = "MEMBER", _("Member")
    MAINTAINER = "MAINTAINER", _("Maintainer")
    OWNER = "OWNER", _("Owner")


OBSERVER_EQUIVALENT = [
    WorkspaceUserRoles.OBSERVER,
    WorkspaceUserRoles.MEMBER,
    WorkspaceUserRoles.MAINTAINER,
    WorkspaceUserRoles.OWNER,
]
MEMBER_EQUIVALENT = [
    WorkspaceUserRoles.MEMBER,
    WorkspaceUserRoles.MAINTAINER,
    WorkspaceUserRoles.OWNER,
]
MAINTAINER_EQUIVALENT = [
    WorkspaceUserRoles.MAINTAINER,
    WorkspaceUserRoles.OWNER,
]
OWNER_EQUIVALENT = [
    WorkspaceUserRoles.OWNER,
]


class WorkspaceUser(TimeStampedModel, models.Model):
    """Workspace to user mapping."""

    workspace = models.ForeignKey["Workspace"](
        Workspace,
        on_delete=models.PROTECT,
    )
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
    objects = cast(WorkspaceUserQuerySet, WorkspaceUserQuerySet.as_manager())

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

    objects = cast(WorkspaceBoardQuerySet, WorkspaceBoardQuerySet.as_manager())

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
    objects = cast(
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
                deferrable=models.Deferrable.DEFERRED,  # type:ignore
            )
        ]


class TaskQuerySet(models.QuerySet["Task"]):
    """Manager for Task."""

    def filter_by_workspace(self, workspace: Workspace) -> Self:
        """Filter by workspace."""
        return self.filter(
            workspace_board_section__workspace_board__workspace=workspace,
        )

    def filter_by_assignee(self, assignee: WorkspaceUser) -> Self:
        """Filter by assignee user."""
        return self.filter(assignee=assignee)

    def filter_by_workspace_board_section_pks(
        self,
        workspace_board_section_pks: Pks,
    ) -> Self:
        """Filter by workspace board section pks."""
        return self.filter(
            workspace_board_section__pk__in=workspace_board_section_pks,
        )

    def filter_by_workspace_board(
        self, workspace_board: WorkspaceBoard
    ) -> Self:
        """Filter by tasks contained in workspace board."""
        return self.filter(
            workspace_board_section__workspace_board=workspace_board,
        )

    def filter_for_user_and_uuid(
        self, user: AbstractBaseUser, uuid: uuid.UUID
    ) -> Self:
        """Return task from user workspace corresponding to uuid."""
        return self.filter(
            workspace_board_section__workspace_board__workspace__users=user,
            uuid=uuid,
        )

    # XXX still used?
    def duplicate_task(self, task: "Task") -> "Task":
        """Duplicate a task."""
        new_task = self.create(
            workspace_board_section=task.workspace_board_section,
            title=task.title,
            description=task.description,
            workspace=task.workspace,
        )
        return new_task


@pgtrigger.register(
    pgtrigger.Trigger(
        name="ensure_correct_workspace",
        when=pgtrigger.Before,
        operation=pgtrigger.Insert | pgtrigger.Update,
        func="""
              DECLARE
                correct_workspace_id   INTEGER;
              BEGIN
                SELECT "workspace_workspace"."id" INTO correct_workspace_id
                FROM "workspace_workspace"
                INNER JOIN "workspace_workspaceboard"
                    ON ("workspace_workspace"."id" = \
                    "workspace_workspaceboard"."workspace_id")
                INNER JOIN "workspace_workspaceboardsection"
                    ON ("workspace_workspaceboard"."id" = \
                         "workspace_workspaceboardsection"."workspace_board_id")
                INNER JOIN "workspace_task"
                    ON ("workspace_workspaceboardsection"."id" = \
                        "workspace_task"."workspace_board_section_id")
                WHERE "workspace_task"."id" = NEW.id
                LIMIT 1;
                IF correct_workspace_id != NEW.workspace_id THEN
                    RAISE EXCEPTION 'invalid workspace_id: workspace being \
                        inserted does not match correct derived workspace.';
                END IF;
                RETURN NEW;
              END;""",
    )
)
@pgtrigger.register(
    pgtrigger.Trigger(
        name="read_only_task_number",
        when=pgtrigger.Before,
        operation=pgtrigger.Update,
        func="""
              BEGIN
                IF NEW.number != OLD.number THEN
                    RAISE EXCEPTION 'invalid number: Task number \
                        cannot be modified after inserting Task.';
                END IF;
                RETURN NEW;
              END;""",
    )
)
class Task(
    TitleDescriptionModel,
    TimeStampedModel,
    models.Model,
):
    """Task, belongs to workspace board section."""

    workspace = models.ForeignKey["Workspace"](
        Workspace,
        on_delete=models.CASCADE,
    )

    workspace_board_section = models.ForeignKey["WorkspaceBoardSection"](
        WorkspaceBoardSection,
        on_delete=models.CASCADE,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    assignee = models.ForeignKey["WorkspaceUser"](
        WorkspaceUser,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("Workspace user this task is assigned to."),
    )
    deadline = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Task's deadline"),
    )
    labels = models.ManyToManyField(
        "workspace.Label",
        through="workspace.TaskLabel",
    )  # type: models.ManyToManyField["Label", "TaskLabel"]

    number = models.PositiveIntegerField()

    objects = cast(TaskQuerySet, TaskQuerySet.as_manager())

    if TYPE_CHECKING:
        # Related fields
        subtask_set: RelatedManager["SubTask"]
        chatmessage_set: RelatedManager["ChatMessage"]
        tasklabel_set: RelatedManager["TaskLabel"]

        # Order related
        get_subtask_order: GetOrder
        set_subtask_order: SetOrder
        _order: int

    def move_to(
        self, workspace_board_section: WorkspaceBoardSection, order: int
    ) -> None:
        """
        Move to specified workspace board section and to order n.

        No save required.
        """
        neighbor_tasks = (
            self.workspace_board_section.task_set.select_for_update()
        )
        if self.workspace_board_section != workspace_board_section:
            other_tasks = workspace_board_section.task_set.select_for_update()
        else:
            # Same section, so no need to select other tasks
            other_tasks = None
        with transaction.atomic():
            # Force both querysets to be evaluated to lock them for the time of
            # this transaction
            len(neighbor_tasks)
            if other_tasks:
                len(other_tasks)
            # Set new WorkspaceBoardSection
            if self.workspace_board_section != workspace_board_section:
                self.workspace_board_section = workspace_board_section
                self.save()

            # Change order
            order_list = list(workspace_board_section.get_task_order())
            current_object_index = order_list.index(self.pk)
            order_list.insert(order, order_list.pop(current_object_index))

            # Set the order
            workspace_board_section.set_task_order(order_list)
            workspace_board_section.save()

    def add_sub_task(self, title: str, description: str) -> "SubTask":
        """Add a sub task."""
        return self.subtask_set.create(title=title, description=description)

    def add_chat_message(
        self, text: str, author: AbstractBaseUser
    ) -> "ChatMessage":
        """Add a chat message."""
        workspace_user = WorkspaceUser.objects.get_by_workspace_and_user(
            self.workspace,
            author,
        )
        return self.chatmessage_set.create(text=text, author=workspace_user)

    def assign_to(self, assignee: Optional[AbstractBaseUser]) -> None:
        """
        Assign task to user.

        Saves after done.
        """
        if assignee is not None:
            # Check if assignee is part of the task's workspace
            workspace = self.workspace_board_section.workspace_board.workspace
            workspace_user = WorkspaceUser.objects.get_by_workspace_and_user(
                workspace,
                assignee,
            )
        else:
            workspace_user = None
        # Change assignee
        self.assignee = workspace_user
        # Save
        self.save()

    def get_next_section(self) -> WorkspaceBoardSection:
        """Return instance of the next section."""
        next_section: WorkspaceBoardSection = (
            self.workspace_board_section.get_next_in_order()
        )
        return next_section

    def add_label(self, label: "Label") -> "TaskLabel":
        """
        Add a label to this task.

        Returns task label.
        """
        task_label: TaskLabel
        workspace = self.workspace_board_section.workspace_board.workspace
        # XXX can this be a db constraint?
        assert label.workspace == workspace
        with transaction.atomic():
            if self.tasklabel_set.filter(label=label).exists():
                task_label = self.tasklabel_set.get(label=label)
                return task_label
            task_label = self.tasklabel_set.create(label=label)
            return task_label

    def remove_label(self, label: "Label") -> "Label":
        """
        Remove a label from this task. Is idempotent.

        Returns label.
        """
        try:
            task_label: TaskLabel = self.tasklabel_set.get(label=label)
            task_label.delete()
        except TaskLabel.DoesNotExist:
            pass
        return label

    # TODO we can probably do better than any here
    def save(self, *args: Any, **kwargs: Any) -> None:
        """Override save to add task number."""
        if self.number is None:
            self.number = self.workspace.increment_highest_task_number()
        super().save(*args, **kwargs)

    class Meta:
        """Meta."""

        order_with_respect_to = "workspace_board_section"
        constraints = [
            models.UniqueConstraint(
                fields=["workspace_board_section", "_order"],
                name="unique_task_order",
                deferrable=models.Deferrable.DEFERRED,  # type:ignore
            ),
            models.UniqueConstraint(
                fields=["workspace", "number"],
                name="unique_task_number",
                deferrable=models.Deferrable.DEFERRED,  # type:ignore
            ),
        ]


class LabelQuerySet(models.QuerySet["Label"]):
    """Label Queryset."""

    def filter_by_workspace_pks(self, workspace_pks: Pks) -> Self:
        """Filter by workspace pks."""
        return self.filter(workspace__pk__in=workspace_pks)

    def filter_for_user_and_uuid(
        self, user: AbstractBaseUser, uuid: uuid.UUID
    ) -> Self:
        """Return for matching workspace user and uuid."""
        return self.filter(workspace__users=user, uuid=uuid)


class Label(models.Model):
    """A label."""

    name = models.CharField(max_length=255)
    color = models.PositiveBigIntegerField(
        help_text=_("Color index"),
        default=0,
    )
    workspace = models.ForeignKey["Workspace"](
        Workspace,
        on_delete=models.CASCADE,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    objects = cast(LabelQuerySet, LabelQuerySet.as_manager())

    class Meta:
        """Meta."""

        unique_together = ("workspace", "name")


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

    objects = cast(TaskLabelQuerySet, TaskLabelQuerySet.as_manager())

    @property
    def workspace(self) -> Workspace:
        """Get workspace instance."""
        return self.label.workspace

    class Meta:
        """Meta."""

        unique_together = ("task", "label")


class SubTaskQuerySet(models.QuerySet["SubTask"]):
    """Sub task queryset."""

    def filter_by_task_pks(self, task_pks: Pks) -> Self:
        """Filter by task pks."""
        return self.filter(task__pk__in=task_pks)

    def filter_for_user_and_uuid(
        self, user: AbstractBaseUser, uuid: uuid.UUID
    ) -> Self:
        """Get sub task for a certain user and sub task uuid."""
        kwargs = {
            "task__workspace_board_section__workspace_board__"
            "workspace__users": user,
            "uuid": uuid,
        }
        return self.filter(**kwargs)


class SubTask(
    TitleDescriptionModel,
    TimeStampedModel,
    models.Model,
):
    """SubTask, belongs to Task."""

    task = models.ForeignKey["Task"](
        Task,
        on_delete=models.CASCADE,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    done = models.BooleanField(
        default=False,
        help_text=_("Designate whether this sub task is done"),
    )

    objects = cast(SubTaskQuerySet, SubTaskQuerySet.as_manager())

    # Ordering related
    _order: int

    def move_to(self, order: int) -> None:
        """
        Move to specified order n within task.

        No save required.
        """
        neighbor_subtasks = self.task.subtask_set.select_for_update()
        with transaction.atomic():
            # Force queryset to be evaluated to lock them for the time of
            # this transaction
            len(neighbor_subtasks)
            current_task = self.task
            # Django docs wrong, need to cast to list
            order_list = list(current_task.get_subtask_order())
            # The list is ordered by pk, which is not uuid for us
            current_object_index = order_list.index(self.pk)
            # Mutate to perform move operation
            order_list.insert(order, order_list.pop(current_object_index))
            # Set new order
            current_task.set_subtask_order(order_list)
            current_task.save()

    @property
    def workspace(self) -> Workspace:
        """Get workspace instance."""
        return self.task.workspace_board_section.workspace_board.workspace

    class Meta:
        """Meta."""

        order_with_respect_to = "task"
        constraints = [
            models.UniqueConstraint(
                fields=["task", "_order"],
                name="unique_sub_task_order",
                deferrable=models.Deferrable.DEFERRED,  # type:ignore
            )
        ]


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
    objects = cast(ChatMessageQuerySet, ChatMessageQuerySet.as_manager())

    @property
    def workspace(self) -> Workspace:
        """Get workspace instance."""
        return self.task.workspace_board_section.workspace_board.workspace

    class Meta:
        """Meta."""

        ordering = ("created",)
