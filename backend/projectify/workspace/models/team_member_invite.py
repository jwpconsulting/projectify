# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Contains team member invite qs / manager / model."""

from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _

from projectify.lib.models import BaseModel
from projectify.user.models import UserInvite

if TYPE_CHECKING:
    from ..models import Workspace  # noqa


class TeamMemberInvite(BaseModel):
    """UserInvites belonging to this workspace."""

    user_invite = models.ForeignKey[UserInvite](
        "user.UserInvite",
        on_delete=models.CASCADE,
    )
    workspace = models.ForeignKey["Workspace"](
        "Workspace",
        on_delete=models.CASCADE,
    )
    # TODO use redeemed_when only
    redeemed = models.BooleanField(
        default=False,
        help_text=_("Has this invite been redeemed?"),
    )
    redeemed_when = models.DateTimeField(
        blank=True,
        null=True,
        editable=False,
        default=None,
        help_text=_("When has this invite been redeemed?"),
    )

    class Meta:
        """Meta."""

        unique_together = ("user_invite", "workspace")
