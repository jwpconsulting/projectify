# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Project model selectors."""

from typing import Optional
from uuid import UUID

from django.db.models import Count, Prefetch, Q, QuerySet
from django.db.models.functions import NullIf

from projectify.user.models import User
from projectify.workspace.models.task import Task

from ..models.project import Project


def project_detail_query_set(
    *,
    team_member_uuids: Optional[list[UUID]] = None,
    label_uuids: Optional[list[UUID]] = None,
) -> QuerySet[Project]:
    """Create a project detail query set."""
    task_qs = Task.objects.annotate(
        sub_task_progress=Count(
            "subtask",
            filter=Q(subtask__done=True),
        )
        * 1.0
        / NullIf(Count("subtask"), 0),
    ).order_by("_order")
    if team_member_uuids:
        task_qs = task_qs.filter(
            assignee__uuid__in=team_member_uuids,
        )
    if label_uuids:
        # XXX this might not work
        task_qs = task_qs.filter(
            label__in=label_uuids,
        )
    return Project.objects.prefetch_related(
        "section_set",
        Prefetch("section_set__task_set", queryset=task_qs),
        "section_set__task_set__assignee",
        "section_set__task_set__assignee__user",
        "section_set__task_set__labels",
        "workspace__label_set",
        Prefetch(
            "workspace__project_set",
            queryset=Project.objects.filter(archived__isnull=True),
        ),
        "workspace__teammember_set",
        "workspace__teammember_set__user",
    )


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
