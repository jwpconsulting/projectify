"""Workspace factories."""
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


class TaskFactory(django.DjangoModelFactory):
    """Task factory."""

    title = factory.Faker("word")
    description = factory.Faker("paragraph")
    workspace_board_section = factory.SubFactory(WorkspaceBoardSectionFactory)

    class Meta:
        """Meta."""

        model = models.Task


class SubTaskFactory(django.DjangoModelFactory):
    """SubTask Factory."""

    title = factory.Faker("word")
    description = factory.Faker("paragraph")
    task = factory.SubFactory(TaskFactory)

    class Meta:
        """Meta."""

        model = models.SubTask
