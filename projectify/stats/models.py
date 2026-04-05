# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Stats app models."""

from django.db import models

from projectify.lib.models import BaseModel


class DailyCount(BaseModel):
    """Daily count for a name."""

    name = models.CharField(max_length=2048)
    date = models.DateField()
    count = models.PositiveIntegerField(default=0)

    class Meta:
        """Meta options."""

        constraints = [
            models.UniqueConstraint(
                fields=["name", "date"],
                name="unique_name_date",
                deferrable=models.Deferrable.DEFERRED,
            )
        ]
