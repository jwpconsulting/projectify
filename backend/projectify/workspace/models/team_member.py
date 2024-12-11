# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Team member models."""

import uuid
from typing import TYPE_CHECKING, ClassVar, Self, cast

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from projectify.lib.models import BaseModel

from .const import TeamMemberRoles
from .types import Pks
from .workspace import Workspace

# TODO Here we could be using __all__


if TYPE_CHECKING:
    from django.db.models.fields.related import RelatedField  # noqa: F401

    from projectify.user.models import User, UserInvite  # noqa: F401


class TeamMemberQuerySet(models.QuerySet["TeamMember"]):
    """Team member queryset."""

    def filter_by_workspace_pks(self, workspace_pks: Pks) -> Self:
        """Filter by workspace pks."""
        return self.filter(workspace__pk__in=workspace_pks)

    def filter_by_user(self, user: AbstractBaseUser) -> Self:
        """Filter team members based on this user's workspaces."""
        return self.filter(workspace__users=user)


class TeamMember(BaseModel):
    """Workspace to user mapping."""

    workspace = models.ForeignKey["Workspace"](
        Workspace,
        on_delete=models.PROTECT,
    )
    # This defo depends on the User in user/ app
    user = models.ForeignKey["User"](
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    role = models.CharField(
        max_length=11,
        choices=TeamMemberRoles.choices,
        default=TeamMemberRoles.OBSERVER,
    )
    job_title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    # Sort of nonsensical
    objects: ClassVar[TeamMemberQuerySet] = cast(  # type: ignore[assignment]
        TeamMemberQuerySet, TeamMemberQuerySet.as_manager()
    )

    if TYPE_CHECKING:
        # Related
        user_invite: RelatedField[None, "UserInvite"]

    def assign_role(self, role: str) -> None:
        """
        Assign a new role.

        Saves.
        """
        self.role = role
        self.save()

    def __str__(self) -> str:
        """Return title."""
        return self.user.email

    class Meta:
        """Meta."""

        unique_together = ("workspace", "user")
