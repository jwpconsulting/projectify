# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Workspace model selectors."""

import logging
from typing import Optional
from uuid import UUID

from django.db.models import (
    BooleanField,
    ExpressionWrapper,
    Prefetch,
    Q,
    QuerySet,
)

from projectify.user.models import User

from ..models.project import Project
from ..models.team_member import TeamMember
from ..models.team_member_invite import TeamMemberInvite
from ..models.workspace import Workspace

logger = logging.getLogger(__name__)


def workspace_build_detail_query_set(
    *, who: Optional[User]
) -> QuerySet[Workspace]:
    """
    Build workspace detail query set.

    Optionally annotate if team member is the same user as `who`.
    """
    teammember_prefetch: Prefetch[TeamMember]
    if who is None:
        teammember_prefetch = Prefetch(
            "teammember_set",
            queryset=TeamMember.objects.select_related("user"),
        )
    else:
        teammember_prefetch = Prefetch(
            "teammember_set",
            queryset=TeamMember.objects.select_related("user").annotate(
                is_current_user=ExpressionWrapper(
                    Q(user=who),
                    output_field=BooleanField(),
                )
            ),
        )
    qs = Workspace.objects.prefetch_related(
        "label_set",
    ).prefetch_related(
        Prefetch(
            "project_set",
            queryset=Project.objects.filter(archived__isnull=True),
        ),
        teammember_prefetch,
        Prefetch(
            "teammemberinvite_set",
            # Is there a privacy impact in having a workspace be able to resolve
            # ws -> ws user invite -> user invite?
            # Is there a way one can smuggle a resolution like
            # ws -> ws user invite -> user invite -> other ws's user invite ->
            # other ws and so on?
            # Perhaps only if RCE exists, but then we have different problems...
            queryset=TeamMemberInvite.objects.select_related(
                "user_invite"
            ).filter(redeemed=False),
        ),
    )
    return qs


WorkspaceDetailQuerySet = workspace_build_detail_query_set(who=None)


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
