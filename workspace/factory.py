"""Workspace factories."""
from datetime import (
    timezone,
)

import factory
from factory import (
    django,
)
from user.factory import (
    UserFactory,
)

from . import (
    models,
)


class WorkspaceFactory(django.DjangoModelFactory):
    """Workspace Factory."""

    title = factory.Faker("word")
    description = factory.Faker("paragraph")

    @factory.post_generation
    def add_users(self, created, extracted, *args, **kwargs):
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


class WorkspaceUserFactory(django.DjangoModelFactory):
    """WorkspaceUser factory."""

    user = factory.SubFactory(UserFactory)
    workspace = factory.SubFactory(WorkspaceFactory)

    class Meta:
        """Meta."""

        model = models.WorkspaceUser


class WorkspaceBoardFactory(django.DjangoModelFactory):
    """WorkspaceBoard factory."""

    title = factory.Faker("word")
    description = factory.Faker("paragraph")
    workspace = factory.SubFactory(WorkspaceFactory)

    class Meta:
        """Meta."""

        model = models.WorkspaceBoard


class WorkspaceBoardSectionFactory(django.DjangoModelFactory):
    """WorkspaceBoard Section Factory."""

    title = factory.Faker("word")
    description = factory.Faker("paragraph")
    workspace_board = factory.SubFactory(WorkspaceBoardFactory)

    class Meta:
        """Meta."""

        model = models.WorkspaceBoardSection


def extract_assignee(task):
    """Extract author from chat_message by walking through workspace."""
    workspace_board = task.workspace_board_section.workspace_board
    workspace_user = workspace_board.workspace.workspaceuser_set.first()
    if not workspace_user:
        workspace_user = WorkspaceUserFactory(
            workspace=workspace_board.workspace,
        )
    user = workspace_user.user
    return user


class TaskFactory(django.DjangoModelFactory):
    """Task factory."""

    title = factory.Faker("word")
    description = factory.Faker("paragraph")
    workspace_board_section = factory.SubFactory(WorkspaceBoardSectionFactory)
    assignee = factory.LazyAttribute(extract_assignee)
    deadline = factory.Faker("date_time", tzinfo=timezone.utc)

    class Meta:
        """Meta."""

        model = models.Task


class LabelFactory(django.DjangoModelFactory):
    """Factory for Label."""

    name = factory.Faker("catch_phrase")
    color = factory.Faker("safe_color_name")
    workspace = factory.SubFactory(WorkspaceFactory)

    class Meta:
        """Meta."""

        model = models.Label


class SubTaskFactory(django.DjangoModelFactory):
    """SubTask Factory."""

    title = factory.Faker("word")
    description = factory.Faker("paragraph")
    task = factory.SubFactory(TaskFactory)
    done = False

    class Meta:
        """Meta."""

        model = models.SubTask


def extract_author(chat_message):
    """Extract author from chat_message by walking through workspace."""
    workspace_board = chat_message.task.workspace_board_section.workspace_board
    workspace_user = workspace_board.workspace.workspaceuser_set.first()
    if not workspace_user:
        workspace_user = WorkspaceUserFactory(
            workspace=workspace_board.workspace,
        )
    user = workspace_user.user
    return user


class ChatMessageFactory(django.DjangoModelFactory):
    """ChatMessage Factory."""

    task = factory.SubFactory(TaskFactory)
    text = factory.Faker("paragraph")
    author = factory.LazyAttribute(extract_author)

    class Meta:
        """Meta."""

        model = models.ChatMessage
