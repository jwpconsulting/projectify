# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
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
"""Contains enums and other constant values."""
from django.db import (
    models,
)
from django.utils.translation import gettext_lazy as _


class WorkspaceUserRoles(models.TextChoices):
    """Roles available."""

    OBSERVER = "OBSERVER", _("Observer")
    MEMBER = "MEMBER", _("Member")
    MAINTAINER = "MAINTAINER", _("Maintainer")
    OWNER = "OWNER", _("Owner")


OBSERVER_EQUIVALENT = [
    WorkspaceUserRoles.OBSERVER,
    WorkspaceUserRoles.MEMBER,
    WorkspaceUserRoles.MAINTAINER,
    WorkspaceUserRoles.OWNER,
]
MEMBER_EQUIVALENT = [
    WorkspaceUserRoles.MEMBER,
    WorkspaceUserRoles.MAINTAINER,
    WorkspaceUserRoles.OWNER,
]
MAINTAINER_EQUIVALENT = [
    WorkspaceUserRoles.MAINTAINER,
    WorkspaceUserRoles.OWNER,
]
OWNER_EQUIVALENT = [
    WorkspaceUserRoles.OWNER,
]
