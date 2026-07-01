# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
"""Workspace model selectors."""

import logging
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from django.db.models import (
    BooleanField,
    Count,
    ExpressionWrapper,
    Prefetch,
    Q,
    QuerySet,
)

from projectify.corporate.types import CustomerSubscriptionStatus
from projectify.user.models import User

from ..models import Project, Task, TeamMember, TeamMemberInvite, Workspace

logger = logging.getLogger(__name__)


def workspace_build_detail_query_set(
    *, who: Optional[User], annotate_task_count: bool = False
) -> QuerySet[Workspace]:
    """
    Build workspace detail query set.

    Optionally annotate if team member is the same user as `who`.
    """
    teammembers = TeamMember.objects.select_related("user")
    if who is not None:
        teammembers = teammembers.annotate(
            is_current_user=ExpressionWrapper(
                Q(user=who), output_field=BooleanField()
            )
        )
    if annotate_task_count:
        project_not_archived = Q(task__project__archived__isnull=True)
        teammembers = teammembers.annotate(
            task_count=Count("task", filter=project_not_archived)
        )
    teammember_prefetch: Prefetch[TeamMember] = Prefetch(
        "teammember_set", queryset=teammembers
    )

    qs = Workspace.objects.prefetch_related(
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


def workspace_find_unpaid_for_user(*, who: User) -> QuerySet[Workspace]:
    """Find unpaid workspaces owned by a given user."""
    return Workspace.objects.filter(
        teammember__user=who,
        teammember__role="OWNER",
        customer__subscription_status=CustomerSubscriptionStatus.UNPAID,
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


@dataclass
class WorkspaceSearchResults:
    """Contain search results for a workspace search."""

    projects: QuerySet[Project]
    tasks: QuerySet[Task]


def workspace_search(
    *,
    workspace: Workspace,
    who: User,
    query: Optional[str],
    filter_by_team_members: Optional[QuerySet[TeamMember]] = None,
    # TODO rename to filter_by_unassigned
    unassigned_tasks: bool = False,
    exclude_task: Optional[UUID] = None,
) -> WorkspaceSearchResults:
    """Search workspace for `query`."""
    workspace_filter = Q(workspace=workspace, workspace__users=who)

    assignee_contained = Q(assignee__in=filter_by_team_members)
    assignee_empty = Q(assignee__isnull=True)

    task_q = workspace_filter & Q(project__archived__isnull=True)

    match filter_by_team_members, unassigned_tasks:
        case None, False:
            task_q &= Q()
        case None, True:
            task_q &= assignee_empty
        case _, False:
            task_q &= assignee_contained
        case _, True:
            task_q &= assignee_contained | assignee_empty

    if query is not None:
        task_q &= Q(title__icontains=query) | Q(description__icontains=query)
    if exclude_task is not None:
        task_q &= ~Q(uuid=exclude_task)
    tasks = (
        Task.objects.filter(task_q)
        .select_related("project", "assignee__user")
        .order_by("project__modified")
    )

    project_q = workspace_filter & Q(archived__isnull=True)
    if query is not None:
        project_q &= Q(title__icontains=query) | Q(
            description__icontains=query
        )
    project_qs = Project.objects.filter(project_q)

    return WorkspaceSearchResults(projects=project_qs, tasks=tasks)
