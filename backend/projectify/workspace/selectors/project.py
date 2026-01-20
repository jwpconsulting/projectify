# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Project model selectors."""

from typing import Optional, Union
from uuid import UUID

from django.db.models import Case, Count, Prefetch, Q, QuerySet, Value, When
from django.db.models.functions import NullIf

from projectify.user.models import User
from projectify.workspace.models.const import COLOR_MAP
from projectify.workspace.models.label import Label
from projectify.workspace.models.task import Task
from projectify.workspace.models.team_member import TeamMember

from ..models.project import Project


# XXX Maybe this should be in selectors/label.py
def _annotate_labels_with_colors(label_qs: QuerySet[Label]) -> QuerySet[Label]:
    """Annotate labels with bg_class and border_class based on COLOR_MAP."""
    bg_cases = [
        When(color=i, then=Value(color_info["bg_class"]))
        for i, color_info in COLOR_MAP.items()
    ]
    border_cases = [
        When(color=i, then=Value(color_info["border_class"]))
        for i, color_info in COLOR_MAP.items()
    ]

    return label_qs.annotate(
        bg_class=Case(*bg_cases, default=Value(COLOR_MAP[0]["bg_class"])),
        border_class=Case(
            *border_cases, default=Value(COLOR_MAP[0]["border_class"])
        ),
    )


def project_detail_query_set(
    *,
    team_member_uuids: Optional[list[UUID]] = None,
    label_uuids: Optional[list[UUID]] = None,
    unassigned_tasks: Optional[bool] = None,
    unlabeled_tasks: Optional[bool] = None,
    task_search_query: Optional[str] = None,
) -> QuerySet[Project]:
    """Create a project detail query set."""
    team_member_qs = TeamMember.objects.select_related("user").annotate(
        task_count=Count("task")
    )
    label_qs = _annotate_labels_with_colors(
        Label.objects.all().annotate(
            task_count=Count("task"),
        )
    )
    task_q = Q()
    assignee_uuid = Q(assignee__uuid__in=team_member_uuids)
    assignee_empty = Q(assignee__isnull=True)
    match team_member_uuids, unassigned_tasks:
        case list(), None:
            task_q = task_q & assignee_uuid
            team_member_qs = team_member_qs.annotate(
                is_filtered=Q(uuid__in=team_member_uuids)
            )
        case None, True:
            task_q = task_q & assignee_empty
        case list(), True:
            task_q = task_q & (assignee_uuid & assignee_empty)
            team_member_qs = team_member_qs.annotate(
                is_filtered=Q(uuid__in=team_member_uuids)
            )
        case _, _:
            pass

    labels_uuid = Q(labels__uuid__in=label_uuids)
    labels_empty = Q(labels__isnull=True)
    label_is_filtered: Union[Value, Q] = Value(False)
    match label_uuids, unlabeled_tasks:
        case list(), None:
            task_q = task_q & labels_uuid
            label_is_filtered = Q(uuid__in=label_uuids)
        case None, True:
            task_q = task_q & labels_empty
        case list(), True:
            task_q = task_q & (labels_uuid | labels_empty)
            label_is_filtered = Q(uuid__in=label_uuids)
        case _, _:
            pass
    label_qs = label_qs.annotate(is_filtered=label_is_filtered)

    if task_search_query is not None:
        task_q = task_q & Q(title__icontains=task_search_query)

    task_qs = (
        Task.objects.annotate(
            sub_task_progress=Count(
                "subtask",
                filter=Q(subtask__done=True),
            )
            * 1.0
            / NullIf(Count("subtask"), 0),
        )
        .order_by("_order")
        .select_related("assignee__user")
        .prefetch_related("labels")
    ).filter(task_q)
    return Project.objects.prefetch_related(
        "section_set",
        Prefetch("section_set__task_set", queryset=task_qs),
        # Prefetch for workspace 1 : N relations, label, projects, and team
        # members
        Prefetch("workspace__label_set", queryset=label_qs),
        Prefetch(
            "workspace__project_set",
            queryset=Project.objects.filter(archived__isnull=True),
        ),
        Prefetch("workspace__teammember_set", queryset=team_member_qs),
    ).select_related("workspace", "workspace__customer")


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
