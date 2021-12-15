"""Workspace factories."""
import factory
from factory import (
    django,
)
from user.factory import (
    UserFactory,
)

from .models import (
    Workspace,
    WorkspaceBoard,
    WorkspaceUser,
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

        model = Workspace


class WorkspaceUserFactory(django.DjangoModelFactory):
    """WorkspaceUser factory."""

    user = factory.SubFactory(UserFactory)
    workspace = factory.SubFactory(WorkspaceFactory)

    class Meta:
        """Meta."""

        model = WorkspaceUser


class WorkspaceBoardFactory(django.DjangoModelFactory):
    """WorkspaceBoard factory."""

    title = factory.Faker("word")
    description = factory.Faker("paragraph")
    workspace = factory.SubFactory(WorkspaceFactory)

    class Meta:
        """Meta."""

        model = WorkspaceBoard
