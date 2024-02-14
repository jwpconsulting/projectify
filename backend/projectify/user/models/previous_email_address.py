# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2024 JWP Consulting GK
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
