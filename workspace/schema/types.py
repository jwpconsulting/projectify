"""Workspace schema types."""
import datetime
import uuid

import strawberry

from user.schema import types as user_types

from .. import (
    models,
)


@strawberry.django.type(models.Workspace)
class Workspace:
    """Workspace."""

    @strawberry.field
    def users(self, info) -> list[user_types.User]:
        """Resolve workspace users."""
        # TODO data loader
        return self.users.all()

    @strawberry.field
    def boards(self) -> list["WorkspaceBoard"]:
        """Resolve workspace boards."""
        # TODO data loader
        return self.workspaceboard_set.filter_by_archived(False)

    @strawberry.field
    def archived_boards(self) -> list["WorkspaceBoard"]:
        """Resolve archived workspace boards."""
        # TODO data loader
        return self.workspaceboard_set.filter_by_archived()

    @strawberry.field
    def labels(self) -> list["Label"]:
        """Resolve labels."""
        # TODO data loadder
        return self.label_set.all()

    @strawberry.field
    def user_invitations(self) -> list["UserInvitation"]:
        """Resolve user invitations."""
        # TODO data loader
        invites = []
        qs = self.workspaceuserinvite_set.filter_by_redeemed(False)
        for invite in qs.iterator():
            invites.append(UserInvitation(email=invite.user_invite.email))
        return invites

    @strawberry.field
    def picture(self) -> str | None:
        """Resolve picture."""
        if self.picture:
            return self.picture.url

    created: datetime.datetime
    modified: datetime.datetime
    title: str
    description: str
    uuid: uuid.UUID


@strawberry.type
class UserInvitation:
    """
    UserInvitation.

    A synthetic object not directly based on a Django model.
    """

    email: str


@strawberry.django.type(models.WorkspaceBoard)
class WorkspaceBoard:
    """WorkspaceBoard."""

    @strawberry.field
    def sections(self, info) -> list["WorkspaceBoardSection"]:
        """Resolve workspace board sections."""
        # TODO data loader
        return self.workspaceboardsection_set.all()

    @strawberry.field
    def workspace(self, info) -> "Workspace":
        """Resolve workspace."""
        return self.workspace

    created: datetime.datetime
    modified: datetime.datetime
    title: str
    description: str
    uuid: uuid.UUID
    archived: datetime.datetime | None
    deadline: datetime.datetime | None


@strawberry.django.type(models.WorkspaceBoardSection)
class WorkspaceBoardSection:
    """WorkspaceBoardSection."""

    @strawberry.field
    def tasks(self) -> list["Task"]:
        """Resolve tasks for this workspace board section."""
        return self.task_set.all()

    @strawberry.field
    def order(self) -> int:
        """Resolve order field."""
        return self._order

    @strawberry.field
    def workspace_board(self) -> "WorkspaceBoard":
        """Resolve workspace board."""
        return self.workspace_board

    created: datetime.datetime
    modified: datetime.datetime
    title: str
    description: str
    uuid: uuid.UUID


@strawberry.django.type(models.Task)
class Task:
    """Task."""

    @strawberry.field
    def sub_tasks(self) -> list["SubTask"]:
        """Resolve sub tasks for this task."""
        # TODO data loader
        return self.subtask_set.all()

    @strawberry.field
    def chat_messages(self) -> list["ChatMessage"]:
        """Resolve chat messages for this task."""
        # TODO data loader
        return self.chatmessage_set.all()

    @strawberry.field
    def workspace_board_section(self) -> "WorkspaceBoardSection":
        """Resolve workspace board section for this task."""
        # TODO data loader
        return self.workspace_board_section

    @strawberry.field
    def next_workspace_board_section(self) -> "WorkspaceBoardSection":
        """Resolve the next section."""
        section = self.get_next_section()
        return section

    @strawberry.field
    def order(self) -> int:
        """Resolve order field."""
        return self._order

    @strawberry.field
    def labels(self) -> list["Label"]:
        """Resolve labels for this task."""
        return self.labels.all()

    @strawberry.field
    def assignee(self) -> user_types.User | None:
        """Resolve user."""
        return self.assignee

    created: datetime.datetime
    modified: datetime.datetime
    title: str
    description: str
    uuid: uuid.UUID


@strawberry.django.type(models.Label)
class Label:
    """Label."""

    @strawberry.field
    def workspace(self) -> Workspace:
        """Resolve workspace."""
        return self.workspace

    name: str
    color: int
    uuid: uuid.UUID


@strawberry.django.type(models.SubTask)
class SubTask:
    """SubTask."""

    @strawberry.field
    def task(self) -> Task:
        """Resolve task with data loader."""
        return self.task

    created: datetime.datetime
    modified: datetime.datetime
    title: str
    description: str
    uuid: uuid.UUID
    order: int
    done: bool


@strawberry.django.type(models.ChatMessage)
class ChatMessage:
    """ChatMessage."""

    @strawberry.field
    def author(self, info) -> user_types.User:
        """Resolve author."""
        return self.author

    created: datetime.datetime
    modified: datetime.datetime
    uuid: uuid.UUID
    text: str
