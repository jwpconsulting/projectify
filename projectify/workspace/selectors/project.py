# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Project model selectors."""

from typing import Any, Optional, Union
from uuid import UUID

from django.db.models import (
    Count,
    Exists,
    OuterRef,
    Prefetch,
    Q,
    QuerySet,
    Value,
)

from projectify.user.models import User

from ..models import Project, Task, TeamMember


def project_detail_query_set(
    *,
    filter_by_team_members: Optional[QuerySet[TeamMember]] = None,
    # TODO rename to filter_by_unassigned
    unassigned_tasks: bool = False,
    task_search_query: Optional[str] = None,
    who: Optional[User] = None,
) -> QuerySet[Project]:
    """Create a project detail query set."""
    project_not_archived = Q(task__project__archived__isnull=True)
    team_member_qs = TeamMember.objects.select_related("user").annotate(
        task_count=Count("task", filter=project_not_archived)
    )
    task_q = Q()

    # Annotate team members in side nav with whether they're filtered or not
    assignee_contained = Q(assignee__in=filter_by_team_members)
    assignee_empty = Q(assignee__isnull=True)
    team_member_is_filtered: Union[Value, Exists] = Value(False)
    match filter_by_team_members, unassigned_tasks:
        case None, False:
            pass
        case None, True:
            task_q = task_q & assignee_empty
        case QuerySet(), False:
            task_q = task_q & assignee_contained
            team_member_is_filtered = Exists(
                filter_by_team_members.filter(pk=OuterRef("pk"))
            )
        case QuerySet(), True:
            task_q = task_q & (assignee_contained | assignee_empty)
            team_member_is_filtered = Exists(
                filter_by_team_members.filter(pk=OuterRef("pk"))
            )
    team_member_qs = team_member_qs.annotate(
        is_filtered=team_member_is_filtered
    )

    if task_search_query is not None:
        task_q = task_q & (
            Q(title__icontains=task_search_query)
            # TODO support querying tasks across projects
            # | Q(project__title__icontains=task_search_query)
        )

    task_qs = Task.objects.select_related("assignee__user").filter(task_q)

    project_prefetches: list[Prefetch[Any]] = [
        # Prefetch for workspace 1 : N relations, projects, and team
        # members
        Prefetch(
            "workspace__project_set",
            queryset=Project.objects.filter(archived__isnull=True),
        ),
        Prefetch("workspace__teammember_set", queryset=team_member_qs),
    ]

    # If caller provides a user, filter out tasks for hidden sections,
    # and mark these sections as minimized
    if who is not None:
        # task_qs = task_qs.exclude(section__minimized_by=who)
        current_team_member_qs = TeamMember.objects.filter(user=who)
        project_prefetches.append(
            Prefetch(
                "workspace__teammember_set",
                queryset=current_team_member_qs,
                to_attr="current_team_member_qs",
            )
        )

    project_prefetches.append(Prefetch("task_set", task_qs))

    project = Project.objects.prefetch_related(
        *project_prefetches
    ).select_related("workspace", "workspace__customer")

    return project


ProjectDetailQuerySet = project_detail_query_set()


def project_find_by_workspace_uuid(
    *, workspace_uuid: UUID, who: User, archived: Optional[bool] = None
) -> QuerySet[Project]:
    """Find projects for a workspace."""
    qs = Project.objects.filter(
        workspace__users=who, workspace__uuid=workspace_uuid
    )
    if archived is not None:
        qs = qs.filter(archived__isnull=not archived)
    return qs


def project_find_by_project_uuid(
    *,
    project_uuid: UUID,
    who: User,
    qs: Optional[QuerySet[Project]] = None,
    archived: bool = False,
) -> Optional[Project]:
    """Find a workspace by uuid for a given user."""
    qs = Project.objects.all() if qs is None else qs
    qs = qs.filter(archived__isnull=not archived)
    qs = qs.filter(workspace__users=who, uuid=project_uuid)
    try:
        return qs.get()
    except Project.DoesNotExist:
        return None
