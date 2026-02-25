# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2025 JWP Consulting GK
"""Label manager and model."""

import uuid
from typing import TYPE_CHECKING, Any

from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint
from django.utils.translation import gettext_lazy as _

from projectify.lib.models import BaseModel

from .workspace import Workspace as Workspace

# TODO Here we could be using __all__


class Label(BaseModel):
    """A label."""

    # TODO It should be fine to just use TitleDescription here
    name = models.CharField(max_length=255)
    """
    0 -> orange
    2 -> pink
    3 -> blue
    4 -> purple
    5 -> yellow
    6 -> red
    7 -> green
    """
    color = models.PositiveBigIntegerField(
        help_text=_("Color index"),
    )
    workspace = models.ForeignKey[Workspace](
        Workspace,
        on_delete=models.CASCADE,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    if TYPE_CHECKING:
        id: int

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Override save and call full_clean."""
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Return name."""
        return self.name

    class Meta:
        """Meta."""

        ordering = ("-modified",)
        constraints = [
            CheckConstraint(
                # type: ignore[call-arg]
                condition=Q(color__gte=0) & Q(color__lte=7),
                name="label_color_range",
                violation_error_message=_("Color must be between 0 and 7"),
            ),
            UniqueConstraint(
                fields=["name", "workspace"],
                name="unique_label_name_per_workspace",
                violation_error_message=_(
                    "You can only create one label with this name."
                ),
            ),
        ]
