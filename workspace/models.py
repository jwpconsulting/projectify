"""Workspace models."""
import uuid

from django.conf import (
    settings,
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
from ordered_model.models import (
    OrderedModel,
    OrderedModelManager,
)
from user import models as user_models

from . import (
    signal_defs,
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
    picture = models.ImageField(
        upload_to="workspace_picture/",
        blank=True,
        null=True,
    )
    objects = WorkspaceManager()

    def add_workspace_board(self, title, description):
        """Add workspace board."""
        return self.workspaceboard_set.create(
            title=title,
            description=description,
        )

    def add_user(self, user):
        """
        Add user to workspace.

        Return user.
        """
        self.workspaceuser_set.create(user=user)
        return user

    @transaction.atomic
    def remove_user(self, user):
        """
        Remove user from workspace.

        Removes the user from task assignments.

        Return user.
        """
        workspace_user = self.workspaceuser_set.get(user=user)
        workspace_user.delete()
        tasks = Task.objects.filter_by_workspace(self).filter_by_assignee(
            user,
        )
        tasks.unset_assignees()
        return user

    @transaction.atomic
    def invite_user(self, email):
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
        workspace_user_invite = self.workspaceuserinvite_set.create(
            user_invite=user_invite,
            workspace=self,
        )
        signal_defs.workspace_user_invited.send(
            sender=self.__class__,
            instance=workspace_user_invite,
        )
        return workspace_user_invite

    @transaction.atomic
    def uninvite_user(self, email):
        """Remove a users invitation."""
        workspace_user_invite = self.workspaceuserinvite_set.get(
            user_invite__email=email,
        )
        workspace_user_invite.delete()


class WorkspaceUserInviteQuerySet(models.QuerySet):
    """QuerySet for WorkspaceUserInvite."""

    def filter_by_workspace_pks(self, workspace_pks):
        """Filter by workspace pks."""
        return self.filter(workspace__pk__in=workspace_pks)

    def filter_by_redeemed(self, redeemed=True):
        """Filter by redeemed workspace user invites."""
        return self.filter(redeemed=redeemed)


class WorkspaceUserInvite(TimeStampedModel, models.Model):
    """UserInvites belonging to this workspace."""

    user_invite = models.ForeignKey(
        "user.UserInvite",
        on_delete=models.CASCADE,
    )
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
    )
    redeemed = models.BooleanField(
        default=False,
        help_text=_("Has this invite been redeemed?"),
    )

    objects = WorkspaceUserInviteQuerySet.as_manager()

    def redeem(self):
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
        on_delete=models.CASCADE,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    objects = WorkspaceUserQuerySet.as_manager()

    class Meta:
        """Meta."""

        unique_together = ("workspace", "user")


class WorkspaceBoardQuerySet(models.QuerySet):
    """WorkspaceBoard Manager."""

    def filter_by_workspace_pks(self, workspace_pks):
        """Filter by workspace pks."""
        return self.filter(workspace__pk__in=workspace_pks)

    def get_for_user_and_uuid(self, user, uuid):
        """Get a workspace baord for user and uuid."""
        return self.filter(workspace__users=user).get(uuid=uuid)

    def filter_by_archived(self, archived=True):
        """Filter by archived boards."""
        return self.filter(archived__isnull=not archived)


class WorkspaceBoard(TitleDescriptionModel, TimeStampedModel, models.Model):
    """Workspace board."""

    workspace = models.ForeignKey(
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

    objects = WorkspaceBoardQuerySet.as_manager()

    def add_workspace_board_section(self, title, description):
        """Add workspace board section to this workspace board."""
        return self.workspaceboardsection_set.create(
            title=title,
            description=description,
        )

    def archive(self):
        """
        Mark this workspace board as archived.

        Saves model instance.
        """
        self.archived = now()
        self.save()

    def unarchive(self):
        """
        Mark this workspace board as not archived.

        Saves model instance.
        """
        self.archived = None
        self.save()


class WorkspaceBoardSectionManager(models.Manager):
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
    TitleDescriptionModel,
    TimeStampedModel,
    models.Model,
):
    """Section of a WorkspaceBoard."""

    workspace_board = models.ForeignKey(
        WorkspaceBoard,
        on_delete=models.CASCADE,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    objects = WorkspaceBoardSectionManager()

    def add_task(self, title, description, deadline=None):
        """Add a task to this section."""
        return self.task_set.create(
            title=title,
            description=description,
            deadline=deadline,
        )

    def move_to(self, order):
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
            current_workspace = self.workspace_board
            # Django docs wrong, need to cast to list
            order_list = list(
                current_workspace.get_workspaceboardsection_order()
            )
            # The list is ordered by pk, which is not uuid for us
            current_object_index = order_list.index(self.pk)
            # Mutate to perform move operation
            order_list.insert(order, order_list.pop(current_object_index))
            # Set new order
            current_workspace.set_workspaceboardsection_order(order_list)
            current_workspace.save()

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


class TaskQuerySet(models.QuerySet):
    """Manager for Task."""

    def filter_by_workspace(self, workspace):
        """Filter by workspace."""
        return self.filter(
            workspace_board_section__workspace_board__workspace=workspace,
        )

    def filter_by_assignee(self, assignee):
        """Filter by assignee user."""
        return self.filter(assignee=assignee)

    def unset_assignees(self):
        """Unset assignees."""
        return self.update(assignee=None)

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

    def duplicate_task(self, task):
        """Duplicate a task."""
        new_task = self.create(
            workspace_board_section=task.workspace_board_section,
            title=task.title,
            description=task.description,
        )
        return new_task


class Task(
    TitleDescriptionModel,
    TimeStampedModel,
    models.Model,
):
    """Task, belongs to workspace board section."""

    workspace_board_section = models.ForeignKey(
        WorkspaceBoardSection,
        on_delete=models.CASCADE,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_("User this task is assigned to."),
    )
    deadline = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Task's deadline"),
    )
    labels = models.ManyToManyField(
        "workspace.Label",
        through="workspace.TaskLabel",
    )

    objects = TaskQuerySet.as_manager()

    def move_to(self, workspace_board_section, order):
        """
        Move to specified workspace board section and to order n.

        No save required.
        """
        neighbor_tasks = (
            self.workspace_board_section.task_set.select_for_update()
        )
        other_tasks = workspace_board_section.task_set.select_for_update()
        with transaction.atomic():
            # Force both querysets to be evaluated to lock them for the time of
            # this transaction
            len(neighbor_tasks)
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

    def add_sub_task(self, title, description):
        """Add a sub task."""
        return self.subtask_set.create(title=title, description=description)

    def add_chat_message(self, text, author):
        """Add a chat message."""
        return self.chatmessage_set.create(
            text=text,
            author=author,
        )

    def assign_to(self, assignee):
        """
        Assign task to user.

        Saves after done.
        """
        if assignee is not None:
            # Check if assignee is part of the task's workspace
            workspace = self.workspace_board_section.workspace_board.workspace
            workspace.users.get(pk=assignee.pk)
        # Change assignee
        self.assignee = assignee
        # Save
        self.save()

    def get_next_section(self):
        """Return instance of the next section."""
        next_section = self.workspace_board_section.get_next_in_order()
        return next_section

    def add_label(self, label):
        """
        Add a label to this task.

        Returns task label.
        """
        workspace = self.workspace_board_section.workspace_board.workspace
        # XXX can this be a db constraint?
        assert label.workspace == workspace
        with transaction.atomic():
            if self.tasklabel_set.filter(label=label).exists():
                return self.tasklabel_set.get(label=label)
            task_label = self.tasklabel_set.create(label=label)
            return task_label

    def remove_label(self, label):
        """
        Remove a label from this task. Is idempotent.

        Returns label.
        """
        try:
            task_label = self.tasklabel_set.get(label=label)
            task_label.delete()
        except TaskLabel.DoesNotExist:
            pass
        return label

    class Meta:
        """Meta."""

        order_with_respect_to = "workspace_board_section"
        constraints = [
            models.UniqueConstraint(
                fields=["workspace_board_section", "_order"],
                name="unique_task_order",
                deferrable=models.Deferrable.DEFERRED,
            )
        ]


class LabelQuerySet(models.QuerySet):
    """Label Queryset."""

    def filter_by_workspace_pks(self, workspace_pks):
        """Filter by workspace pks."""
        return self.filter(workspace__pk__in=workspace_pks)

    def get_for_user_and_uuid(self, user, uuid):
        """Return for matching workspace user and uuid."""
        qs = self.filter(workspace__users=user)
        return qs.get(uuid=uuid)


class Label(models.Model):
    """A label."""

    name = models.CharField(max_length=255)
    color = models.PositiveBigIntegerField(
        help_text=_("Color index"),
        default=0,
    )
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    objects = LabelQuerySet.as_manager()

    class Meta:
        """Meta."""

        unique_together = ("workspace", "name")


class TaskLabelQuerySet(models.QuerySet):
    """QuerySet for TaskLabel."""

    def filter_by_task_pks(self, pks):
        """Filter by task pks."""
        return self.filter(task__pk__in=pks)


class TaskLabel(models.Model):
    """A label to task assignment."""

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
    )
    label = models.ForeignKey(
        Label,
        on_delete=models.CASCADE,
    )

    objects = TaskLabelQuerySet.as_manager()

    class Meta:
        """Meta."""

        unique_together = ("task", "label")


class SubTaskManager(OrderedModelManager):
    """Sub task queryset."""

    def filter_by_task_pks(self, task_pks):
        """Filter by task pks."""
        return self.filter(task__pk__in=task_pks)

    def get_for_user_and_uuid(self, user, uuid):
        """Get sub task for a certain user and sub task uuid."""
        kwargs = {
            "task__workspace_board_section__workspace_board__"
            "workspace__users": user,
        }
        return self.filter(**kwargs).get(uuid=uuid)


class SubTask(
    OrderedModel,
    TitleDescriptionModel,
    TimeStampedModel,
    models.Model,
):
    """SubTask, belongs to Task."""

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    done = models.BooleanField(
        default=False,
        help_text=_("Designate whether this sub task is done"),
    )
    order_with_respect_to = "task"

    objects = SubTaskManager()

    class Meta:
        """Meta."""

        ordering = ("task", "order")


class ChatMessageQuerySet(models.QuerySet):
    """ChatMessage query set."""

    def filter_by_task_pks(self, task_pks):
        """Filter by task pks."""
        return self.filter(task__pk__in=task_pks)

    def get_for_user_and_uuid(self, user, uuid):
        """Get for a specific workspace user and uuid."""
        kwargs = {
            "task__workspace_board_section__workspace_board__"
            "workspace__users": user,
        }
        return self.filter(**kwargs).get(uuid=uuid)


class ChatMessage(TimeStampedModel, models.Model):
    """ChatMessage, belongs to Task."""

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )

    objects = ChatMessageQuerySet.as_manager()

    class Meta:
        """Meta."""

        ordering = ("created",)
