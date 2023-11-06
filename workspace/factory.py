"""Workspace factories."""
from datetime import (
    timezone,
)
from typing import (
    TYPE_CHECKING,
    Iterable,
    Optional,
)

import factory
from factory import (
    django,
)
from user import factory as user_factory

from . import (
    models,
)


if TYPE_CHECKING:
    from user import models as user_models  # noqa: F401


class WorkspaceFactory(django.DjangoModelFactory[models.Workspace]):
    """Workspace Factory."""

    title = factory.Faker("word")
    description = factory.Faker("paragraph")

    @factory.post_generation
    def add_users(
        self,
        created: bool,
        extracted: Iterable["user_models.User"],
    ) -> None:
        """Add users to workspace."""
        if not created:
            return
        if not extracted:
            return
        for user in extracted:
            WorkspaceUserFactory(workspace=self, user=user)

    class Meta:
        """Meta."""

        model = models.Workspace


class WorkspaceUserInviteFactory(
    django.DjangoModelFactory[models.WorkspaceUserInvite]
):
    """WorkspaceUserInvite factory."""

    workspace = factory.SubFactory(WorkspaceFactory)
    user_invite = factory.SubFactory("user.factory.UserInviteFactory")

    class Meta:
        """Meta."""

        model = models.WorkspaceUserInvite


class WorkspaceUserFactory(django.DjangoModelFactory[models.WorkspaceUser]):
    """WorkspaceUser factory."""

    user = factory.SubFactory(user_factory.UserFactory)
    workspace = factory.SubFactory(WorkspaceFactory)
    job_title = factory.Faker("job")

    class Meta:
        """Meta."""

        model = models.WorkspaceUser


class WorkspaceBoardFactory(django.DjangoModelFactory[models.WorkspaceBoard]):
    """WorkspaceBoard factory."""

    title = factory.Faker("word")
    description = factory.Faker("paragraph")
    workspace = factory.SubFactory(WorkspaceFactory)
    deadline = factory.Faker("date_time", tzinfo=timezone.utc)

    class Meta:
        """Meta."""

        model = models.WorkspaceBoard


class WorkspaceBoardSectionFactory(
    django.DjangoModelFactory[models.WorkspaceBoardSection]
):
    """WorkspaceBoard Section Factory."""

    title = factory.Faker("word")
    description = factory.Faker("paragraph")
    workspace_board = factory.SubFactory(WorkspaceBoardFactory)

    class Meta:
        """Meta."""

        model = models.WorkspaceBoardSection


def extract_assignee_workspace_user(task: models.Task) -> models.WorkspaceUser:
    """Extract author from chat_message by walking through workspace."""
    workspace_board = task.workspace_board_section.workspace_board
    workspace_user = workspace_board.workspace.workspaceuser_set.first()
    if not workspace_user:
        workspace_user = WorkspaceUserFactory.create(
            workspace=workspace_board.workspace,
        )
    return workspace_user


def extract_workspace(task: models.Task) -> models.Workspace:
    """Extract author from chat_message by walking through workspace."""
    return task.workspace_board_section.workspace_board.workspace


class TaskFactory(django.DjangoModelFactory[models.Task]):
    """Task factory."""

    title = factory.Faker("word")
    description = factory.Faker("paragraph")
    workspace_board_section = factory.SubFactory(WorkspaceBoardSectionFactory)
    assignee = factory.LazyAttribute(extract_assignee_workspace_user)
    deadline = factory.Faker("date_time", tzinfo=timezone.utc)
    workspace = factory.LazyAttribute(extract_workspace)

    class Meta:
        """Meta."""

        model = models.Task


class LabelFactory(django.DjangoModelFactory[models.Label]):
    """Factory for Label."""

    name = factory.Faker("catch_phrase")
    color = factory.Faker("pyint", min_value=0, max_value=6)
    workspace = factory.SubFactory(WorkspaceFactory)

    class Meta:
        """Meta."""

        model = models.Label


class TaskLabelFactory(django.DjangoModelFactory[models.TaskLabel]):
    """Factory for Label."""

    task = factory.SubFactory(TaskFactory)
    label = factory.SubFactory(LabelFactory)

    class Meta:
        """Meta."""

        model = models.TaskLabel


class SubTaskFactory(django.DjangoModelFactory[models.SubTask]):
    """SubTask Factory."""

    title = factory.Faker("word")
    description = factory.Faker("paragraph")
    task = factory.SubFactory(TaskFactory)
    done = factory.Faker("pybool")

    class Meta:
        """Meta."""

        model = models.SubTask


def extract_author(chat_message: models.ChatMessage) -> models.WorkspaceUser:
    """Extract author from chat_message by walking through workspace."""
    workspace_board = chat_message.task.workspace_board_section.workspace_board
    workspace_user: Optional[
        models.WorkspaceUser
    ] = workspace_board.workspace.workspaceuser_set.first()
    if not workspace_user:
        other_workspace_user: models.WorkspaceUser = (
            WorkspaceUserFactory.create(
                workspace=workspace_board.workspace,
            )
        )
        return other_workspace_user
    return workspace_user


class ChatMessageFactory(django.DjangoModelFactory[models.ChatMessage]):
    """ChatMessage Factory."""

    task = factory.SubFactory(TaskFactory)
    text = factory.Faker("paragraph")
    author = factory.LazyAttribute(extract_author)

    class Meta:
        """Meta."""

        model = models.ChatMessage
