# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023-2024 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Contain workspace model and qs."""
import uuid
from typing import (
    TYPE_CHECKING,
    Optional,
)

from django.conf import (
    settings,
)
from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.db import (
    models,
    transaction,
)

import pgtrigger
from django_extensions.db.models import (
    TitleDescriptionModel,
)

from projectify.lib.models import BaseModel

from ..types import WorkspaceQuota

if TYPE_CHECKING:
    from django.db.models.fields.related import RelatedField  # noqa: F401
    from django.db.models.manager import RelatedManager  # noqa: F401

    from projectify.corporate.models import (
        Customer,
    )

    from . import (
        Label,
        Project,
        TeamMember,
    )
    from .team_member_invite import (
        TeamMemberInvite,
    )


class Workspace(TitleDescriptionModel, BaseModel):
    """Workspace."""

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="TeamMember",
        through_fields=("workspace", "user"),
    )  # type: models.ManyToManyField[AbstractBaseUser, "TeamMember"]
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(
        upload_to="workspace_picture/",
        blank=True,
        null=True,
    )

    highest_task_number = models.IntegerField(default=0)

    # Optional annotation to show trial limits
    # Since it involves additional queries, it is None by default
    quota: Optional[WorkspaceQuota] = None

    if TYPE_CHECKING:
        # Related fields
        customer: RelatedField[None, "Customer"]

        # Related sets
        project_set: RelatedManager["Project"]
        teammember_set: RelatedManager["TeamMember"]
        teammemberinvite_set: RelatedManager["TeamMemberInvite"]
        label_set: RelatedManager["Label"]

    # TODO I wish this worked with TeamMember instead?
    @transaction.atomic
    def remove_user(self, user: AbstractBaseUser) -> AbstractBaseUser:
        """
        Remove user from projectify.workspace.

        Removes the user from task assignments.

        Return user.
        """
        team_member = self.teammember_set.get(user=user)
        team_member.delete()
        return user

    @transaction.atomic
    def increment_highest_task_number(self) -> int:
        """
        Increment and return highest task number.

        Atomic.
        """
        qs = Workspace.objects.filter(pk=self.pk).select_for_update()
        qs.update(highest_task_number=models.F("highest_task_number") + 1)
        return qs.get().highest_task_number

    def __str__(self) -> str:
        """Return title."""
        return self.title

    class Meta:
        """Add triggers."""

        triggers = (
            pgtrigger.Trigger(
                name="ensure_correct_highest_task_number",
                when=pgtrigger.Before,
                operation=pgtrigger.Update,
                func="""
              DECLARE
                max_task_number   INTEGER;
              BEGIN
                SELECT MAX(workspace_task.number) INTO max_task_number
                FROM workspace_task
                WHERE workspace_task.workspace_id = NEW.id;
                IF NEW.highest_task_number < max_task_number THEN
                    RAISE EXCEPTION 'invalid highest_task_number:  \
                    highest_task_number cannot be lower than a task number.';
                END IF;
                RETURN NEW;
              END;""",
            ),
        )
