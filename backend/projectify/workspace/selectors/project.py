# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Project model selectors."""

from typing import Optional, Union
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
from django.db.models.functions import NullIf

from projectify.user.models import User

from ..models.label import Label
from ..models.project import Project
from ..models.section import Section
from ..models.task import Task
from ..models.team_member import TeamMember
from .labels import labels_annotate_with_colors


def project_detail_query_set(
    *,
    filter_by_team_members: Optional[QuerySet[TeamMember]] = None,
    filter_by_labels: Optional[QuerySet[Label]] = None,
    unassigned_tasks: bool = False,
    unlabeled_tasks: bool = False,
    task_search_query: Optional[str] = None,
    who: Optional[User] = None,
) -> QuerySet[Project]:
    """Create a project detail query set."""
    project_not_archived = Q(task__section__project__archived__isnull=True)
    team_member_qs = TeamMember.objects.select_related("user").annotate(
        task_count=Count("task", filter=project_not_archived)
    )
    label_qs = labels_annotate_with_colors(
        Label.objects.all().annotate(
            task_count=Count("tasklabel", filter=project_not_archived),
        )
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
            task_q = task_q & (assignee_contained & assignee_empty)
            team_member_is_filtered = Exists(
                filter_by_team_members.filter(pk=OuterRef("pk"))
            )
    team_member_qs = team_member_qs.annotate(
        is_filtered=team_member_is_filtered
    )

    # Annotate labels shown in side nav with whether they're filtered or not
    label_contained = Q(labels__in=filter_by_labels)
    labels_empty = Q(labels__isnull=True)
    label_is_filtered: Union[Value, Exists] = Value(False)
    match filter_by_labels, unlabeled_tasks:
        case None, False:
            pass
        case None, True:
            task_q = task_q & labels_empty
        case QuerySet(), False:
            task_q = task_q & label_contained
            label_is_filtered = Exists(
                filter_by_labels.filter(pk=OuterRef("pk"))
            )
        case QuerySet(), True:
            task_q = task_q & (label_contained | labels_empty)
            label_is_filtered = Exists(
                filter_by_labels.filter(pk=OuterRef("pk"))
            )
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
        .prefetch_related(
            Prefetch(
                "labels",
                queryset=labels_annotate_with_colors(Label.objects.all()),
            )
        )
    ).filter(task_q)

    # If caller provides a user, filter out tasks for hidden sections,
    if who is not None:
        task_qs = task_qs.exclude(section__minimized_by=who)

    # and mark these sections as minimized
    section_qs = Section.objects.all()
    if who is not None:
        section_qs = section_qs.annotate(
            minimized=Exists(
                Section.objects.filter(pk=OuterRef("pk"), minimized_by=who)
            )
        )

    return Project.objects.prefetch_related(
        Prefetch("section_set", queryset=section_qs),
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
