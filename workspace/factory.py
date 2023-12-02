"""Workspace factories."""
from datetime import (
    timezone,
)
from typing import (
    TYPE_CHECKING,
    Iterable,
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
