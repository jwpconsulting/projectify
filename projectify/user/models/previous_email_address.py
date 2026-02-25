# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""PreviousEmailAddress stores historical email addresses."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from projectify.lib.models import BaseModel
from projectify.user.models.user import User


class PreviousEmailAddress(BaseModel):
    """Store a previous email address that was associated with a user."""

    user = models.ForeignKey[User](
        User,
        on_delete=models.CASCADE,
        help_text=_("User this email address belongs to"),
    )
    email = models.EmailField(help_text=_("Previous email address"))

    def __str__(self) -> str:
        """Return email."""
        return self.email
