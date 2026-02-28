# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Section model."""

import uuid
from typing import TYPE_CHECKING, Callable

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from projectify.lib.models import BaseModel, TitleDescriptionModel

from .types import GetOrder, SetOrder

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager  # noqa: F401

    from projectify.user.models import User  # noqa: F401

    from . import (
        Project,  # noqa: F401
        Task,
    )


class Section(TitleDescriptionModel, BaseModel):
    """Section of a Project."""

    project = models.ForeignKey["Project"]("Project", on_delete=models.CASCADE)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    minimized_by = models.ManyToManyField(
        "user.User",
        blank=True,
        related_name="minimized_sections",
        help_text=_("Users who have minimized this section"),
    )  # type: models.ManyToManyField[User, "Section"]

    if TYPE_CHECKING:
        # Related managers
        task_set: RelatedManager["Task"]

        # For ordering
        get_task_order: GetOrder
        set_task_order: SetOrder
        get_next_in_order: Callable[[], "Section"]
        _order: int

    def __str__(self) -> str:
        """Return title."""
        return self.title

    def get_absolute_url(self) -> str:
        """Get URL to section within project."""
        return f"{reverse('dashboard:projects:detail', args=(str(self.project.uuid),))}#section-{self.uuid}"

    class Meta:
        """Meta."""

        order_with_respect_to = "project"
        constraints = [
            models.UniqueConstraint(
                fields=["project", "_order"],
                name="unique_project_order",
                deferrable=models.Deferrable.DEFERRED,
            )
        ]
