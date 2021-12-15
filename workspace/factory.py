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
    WorkspaceUser,
)


class WorkspaceFactory(django.DjangoModelFactory):
    """Workspace Factory."""

    @factory.post_generation
    def add_users(self, created, extracted, *args, **kwargs):
        """Add users to workspace."""
        if not created:
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
