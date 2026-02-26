# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""User invite model in user app."""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from projectify.lib.models import BaseModel

from .user import User


class UserInvite(BaseModel):
    """User invite model."""

    email = models.EmailField(
        verbose_name=_("Email"),
    )
    user = models.ForeignKey[User](
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text=_("Matched user"),
    )
    redeemed = models.BooleanField(
        default=False,
        help_text=_("Has this invite been redeemed?"),
    )
    # TODO add redeemed_when
