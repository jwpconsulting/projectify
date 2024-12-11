# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Chat message model."""

import uuid
from typing import ClassVar, Self, cast

from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from projectify.lib.models import BaseModel

from .task import Task
from .team_member import TeamMember
from .types import Pks


class ChatMessageQuerySet(models.QuerySet["ChatMessage"]):
    """ChatMessage query set."""

    def filter_by_task_pks(self, task_pks: Pks) -> Self:
        """Filter by task pks."""
        return self.filter(task__pk__in=task_pks)

    def filter_for_user_and_uuid(
        self, user: AbstractBaseUser, uuid: uuid.UUID
    ) -> Self:
        """Get for a specific team member and uuid."""
        kwargs = {
            "task__section__project__" "workspace__users": user,
            "uuid": uuid,
        }
        return self.filter(**kwargs)


class ChatMessage(BaseModel):
    """ChatMessage, belongs to Task."""

    task = models.ForeignKey["Task"](
        Task,
        on_delete=models.CASCADE,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    author = models.ForeignKey["TeamMember"](
        TeamMember,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    # XXX
    objects: ClassVar[ChatMessageQuerySet] = cast(  # type: ignore[assignment]
        ChatMessageQuerySet, ChatMessageQuerySet.as_manager()
    )

    class Meta:
        """Meta."""

        ordering = ("created",)
