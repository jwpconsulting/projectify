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

from ..models import Label, Project, TeamMember, TeamMemberInvite, Workspace
from .labels import labels_annotate_with_colors

logger = logging.getLogger(__name__)


def workspace_build_detail_query_set(
    *, who: Optional[User], annotate_labels: bool = False
) -> QuerySet[Workspace]:
    """
    Build workspace detail query set.

    Optionally annotate if team member is the same user as `who`.
    """
    teammembers = TeamMember.objects.select_related("user")
    if who is not None:
        teammembers = teammembers.annotate(
            is_current_user=ExpressionWrapper(
                Q(user=who),
                output_field=BooleanField(),
            )
        )
    teammember_prefetch: Prefetch[TeamMember] = Prefetch(
        "teammember_set", queryset=teammembers
    )

    labels: QuerySet[Label] = Label.objects.all()
    if annotate_labels:
        labels = labels_annotate_with_colors(Label.objects.all())

    qs = Workspace.objects.prefetch_related(
        Prefetch("label_set", labels),
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
            to_attr="active_invites",
        ),
    )

    if who is not None:
        current_team_member_qs_qs = TeamMember.objects.filter(user=who)
        qs = qs.prefetch_related(
            Prefetch(
                "teammember_set",
                queryset=current_team_member_qs_qs,
                to_attr="current_team_member_qs",
            )
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
