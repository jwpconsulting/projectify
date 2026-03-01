# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Workspace selectors."""

from typing import Optional
from uuid import UUID

from django.db.models import (
    Count,
    OuterRef,
    Prefetch,
    Q,
    QuerySet,
    Subquery,
    Value,
)

from projectify.user.models import User

from ..models import ChatMessage, Label, Project, Task, TeamMember
from .labels import labels_annotate_with_colors

TaskDetailQuerySet: QuerySet[Task] = (
    Task.objects.select_related(
        "workspace",
        "assignee",
        "assignee__user",
    )
    .prefetch_related(
        "subtask_set",
        Prefetch(
            "labels",
            queryset=labels_annotate_with_colors(Label.objects.all()),
        ),
        Prefetch(
            "workspace__label_set",
            queryset=labels_annotate_with_colors(
                Label.objects.annotate(task_count=Count("task"))
            ),
        ),
        Prefetch(
            "workspace__teammember_set",
            queryset=TeamMember.objects.select_related("user").annotate(
                task_count=Count(
                    "task",
                    filter=Q(task__section__project__archived__isnull=True),
                )
            ),
        ),
        Prefetch(
            "chatmessage_set",
            queryset=ChatMessage.objects.select_related(
                "author",
                "author__user",
            ),
        ),
        Prefetch(
            "workspace__project_set",
            queryset=Project.objects.filter(archived__isnull=True),
        ),
    )
    .annotate(
        first=Q(_order=Value(0)),
        last=Q(
            _order=Subquery(
                # The order of the last task in this section
                Task.objects.filter(section_id=OuterRef("section_id"))
                .order_by("-_order")
                .values("_order")[:1]
            )
        ),
    )
)


def task_find_by_task_uuid(
    *, task_uuid: UUID, who: User, qs: Optional[QuerySet[Task]] = None
) -> Optional[Task]:
    """Find a task given a user and uuid."""
    # Special care is needed, one can't write qs or Task.objects since that
    # would cause the given qs to be prematurely evaluated
    qs = Task.objects if qs is None else qs
    try:
        return qs.get(
            section__project__workspace__users=who,
            uuid=task_uuid,
        )
    except Task.DoesNotExist:
        return None
