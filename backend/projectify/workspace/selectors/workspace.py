# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023-2024 JWP Consulting GK
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
"""Workspace model selectors."""
import logging
from typing import Optional
from uuid import UUID

from django.db.models import Prefetch, QuerySet

from projectify.user.models import User

from ..models.project import Project
from ..models.team_member import TeamMember
from ..models.team_member_invite import TeamMemberInvite
from ..models.workspace import Workspace

logger = logging.getLogger(__name__)

WorkspaceDetailQuerySet = Workspace.objects.prefetch_related(
    "label_set",
).prefetch_related(
    Prefetch(
        "project_set",
        queryset=Project.objects.filter(archived__isnull=True),
    ),
    Prefetch(
        "teammember_set",
        queryset=TeamMember.objects.select_related("user"),
    ),
    Prefetch(
        "teammemberinvite_set",
        # Is there a privacy impact in having a workspace be able to resolve
        # ws -> ws user invite -> user invite?
        # Is there a way one can smuggle a resolution like
        # ws -> ws user invite -> user invite -> other ws's user invite ->
        # other ws and so on?
        # Perhaps only if RCE exists, but then we have different problems...
        queryset=TeamMemberInvite.objects.select_related("user_invite").filter(
            redeemed=False
        ),
    ),
)


def workspace_find_for_user(
    *, who: User, qs: Optional[QuerySet[Workspace]] = None
) -> QuerySet[Workspace]:
    """Filter by user."""
    if qs is None:
        qs = Workspace.objects.all()
    return qs.filter(users=who)


def workspace_find_by_workspace_uuid(
    *,
    workspace_uuid: UUID,
    who: User,
    qs: Optional[QuerySet[Workspace]] = None,
) -> Optional[Workspace]:
    """Find a workspace by uuid for a given user."""
    qs = workspace_find_for_user(who=who, qs=qs)
    qs = qs.filter(uuid=workspace_uuid)
    try:
        return qs.get()
    except Workspace.DoesNotExist:
        logger.warning("No workspace found for uuid %s", workspace_uuid)
        return None
