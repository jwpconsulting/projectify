"""Workspace schema types."""
import datetime
import enum
import uuid
from typing import (
    cast,
)

import strawberry

from graphql import (
    GraphQLResolveInfo,
)
from projectify import (
    utils,
)

from .. import (
    models,
)


@strawberry.django.type(models.Workspace)
class Workspace:
    """Workspace."""

    @strawberry.field
    def users(self, info: GraphQLResolveInfo) -> list["WorkspaceUser"]:
        """Resolve workspace users."""
        # TODO data loader
        return self.workspaceuser_set.all()

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
            # workspace/schema/types.py:58: error: Unexpected keyword argument "email" for "UserInvitation"  [call-arg]
            # Why??? XXX Justus 2023-09-08
            i = UserInvitation(email=invite.user_invite.email)
            invites.append(i)
        return invites

    @strawberry.field
    def picture(self) -> str | None:
        """Resolve picture."""
        workspace = cast(models.Workspace, self)
        return utils.crop_image(workspace.picture, 100, 100)

    created: datetime.datetime
    modified: datetime.datetime
    title: str
    description: str
    uuid: uuid.UUID


@strawberry.enum
class WorkspaceUserRole(enum.Enum):
    """Workspace user role enum."""

    OBSERVER = "OBSERVER"
    MEMBER = "MEMBER"
    MAINTAINER = "MAINTAINER"
    OWNER = "OWNER"


@strawberry.django.type(models.WorkspaceUser)
class WorkspaceUser:
    """WorkspaceUser."""

    @strawberry.field
    def email(self) -> str:
        """Resolve email."""
        return self.user.email

    @strawberry.field
    def full_name(self) -> str | None:
        """Resolve full name."""
        return self.user.full_name

    @strawberry.field
    def profile_picture(self) -> str | None:
        """Resolve profile picture."""
        profile_picture = self.user.profile_picture
        return utils.crop_image(profile_picture, 100, 100)

    @strawberry.field
    def role(self) -> WorkspaceUserRole:
        """Resolve user role."""
        if self.role == "OBSERVER":
            return WorkspaceUserRole.OBSERVER
        elif self.role == "MEMBER":
            return WorkspaceUserRole.MEMBER
        elif self.role == "MAINTAINER":
            return WorkspaceUserRole.MAINTAINER
        elif self.role == "OWNER":
            return WorkspaceUserRole.OWNER
        else:
            raise ValueError()

    job_title: str | None
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
    def sections(
        self, info: GraphQLResolveInfo
    ) -> list["WorkspaceBoardSection"]:
        """Resolve workspace board sections."""
        # TODO data loader
        return self.workspaceboardsection_set.all()

    @strawberry.field
    def workspace(self, info: GraphQLResolveInfo) -> "Workspace":
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
    def assignee(self) -> WorkspaceUser | None:
        """Resolve user."""
        return self.assignee

    created: datetime.datetime
    modified: datetime.datetime
    title: str
    description: str
    uuid: uuid.UUID
    deadline: datetime.datetime | None
    number: int


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

    @strawberry.field
    def order(self) -> int:
        """Resolve order field."""
        return self._order

    created: datetime.datetime
    modified: datetime.datetime
    title: str
    description: str
    uuid: uuid.UUID
    done: bool


@strawberry.django.type(models.ChatMessage)
class ChatMessage:
    """ChatMessage."""

    created: datetime.datetime
    modified: datetime.datetime
    uuid: uuid.UUID
    text: str
    author: WorkspaceUser | None
