"""Workspace factories."""
from typing import (
    TYPE_CHECKING,
    Iterable,
    cast,
)

import factory
from factory import (
    django,
)

from workspace.models.workspace import Workspace
from workspace.services.workspace import workspace_add_user

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
            workspace_add_user(
                workspace=cast(Workspace, self), role="OBSERVER", user=user
            )

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
