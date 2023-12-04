"""Chat message model."""
import uuid
from typing import (
    ClassVar,
    Self,
    cast,
)

from django.contrib.auth.models import AbstractBaseUser
from django.db import (
    models,
)

from django_extensions.db.models import (
    TimeStampedModel,
)

from .task import (
    Task,
)
from .types import Pks
from .workspace_user import (
    WorkspaceUser,
)


class ChatMessageQuerySet(models.QuerySet["ChatMessage"]):
    """ChatMessage query set."""

    def filter_by_task_pks(self, task_pks: Pks) -> Self:
        """Filter by task pks."""
        return self.filter(task__pk__in=task_pks)

    def filter_for_user_and_uuid(
        self, user: AbstractBaseUser, uuid: uuid.UUID
    ) -> Self:
        """Get for a specific workspace user and uuid."""
        kwargs = {
            "task__workspace_board_section__workspace_board__"
            "workspace__users": user,
            "uuid": uuid,
        }
        return self.filter(**kwargs)


class ChatMessage(TimeStampedModel, models.Model):
    """ChatMessage, belongs to Task."""

    task = models.ForeignKey["Task"](
        Task,
        on_delete=models.CASCADE,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    author = models.ForeignKey["WorkspaceUser"](
        WorkspaceUser,
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
