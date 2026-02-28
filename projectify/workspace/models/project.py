# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021-2024 JWP Consulting GK
"""Project model."""

import uuid
from typing import TYPE_CHECKING

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from projectify.lib.models import BaseModel, TitleDescriptionModel

from .workspace import Workspace

# TODO Here we could be using __all__


if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager  # noqa: F401

    from . import Section
    from .types import GetOrder, SetOrder


class Project(TitleDescriptionModel, BaseModel):
    """Project."""

    workspace = models.ForeignKey["Workspace"](
        Workspace,
        on_delete=models.PROTECT,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    archived = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Archival timestamp of this workspace board."),
    )
    due_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Due date for this workspace board"),
    )

    if TYPE_CHECKING:
        # Related managers
        section_set: RelatedManager["Section"]

        # For ordering
        get_section_order: GetOrder
        set_section_order: SetOrder

    def __str__(self) -> str:
        """Return title."""
        return self.title

    def get_absolute_url(self) -> str:
        """Return the absolute URL for this project."""
        return reverse(
            "dashboard:projects:detail", kwargs={"project_uuid": self.uuid}
        )

    class Meta:
        """Order by created, descending."""

        ordering = ("-created",)
