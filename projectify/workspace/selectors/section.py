# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2026 JWP Consulting GK
"""Section selectors."""

from typing import Optional
from uuid import UUID

from django.db.models import Count, Prefetch, Q, QuerySet
from django.db.models.functions import NullIf

from projectify.user.models import User

from ..models import Label, Project, Section, Task, TeamMember
from ..selectors.labels import labels_annotate_with_colors

SectionDetailQuerySet = Section.objects.prefetch_related(
    Prefetch(
        "task_set",
        queryset=Task.objects.annotate(
            sub_task_progress=Count(
                "subtask",
                filter=Q(subtask__done=True),
            )
            * 1.0
            / NullIf(Count("subtask"), 0),
        ).order_by("_order"),
    ),
    "task_set__assignee",
    "task_set__assignee__user",
    Prefetch(
        "task_set__labels",
        queryset=labels_annotate_with_colors(Label.objects.all()),
    ),
    "task_set__subtask_set",
    Prefetch(
        "project__workspace__project_set",
        queryset=Project.objects.filter(archived__isnull=True),
    ),
    Prefetch(
        "project__workspace__label_set",
        queryset=labels_annotate_with_colors(
            Label.objects.annotate(task_count=Count("task"))
        ),
    ),
    Prefetch(
        "project__workspace__teammember_set",
        queryset=TeamMember.objects.select_related("user").annotate(
            task_count=Count(
                "task",
                filter=Q(task__section__project__archived__isnull=True),
            )
        ),
    ),
).select_related(
    "project",
    "project__workspace",
)


def section_find_for_user_and_uuid(
    *,
    section_uuid: UUID,
    user: User,
    qs: Optional[QuerySet[Section]] = None,
) -> Optional[Section]:
    """
    Find a section given a UUID and a user.

    Allows specifying optional base queryset.
    """
    if qs is None:
        qs = Section.objects
    try:
        return qs.filter(
            project__workspace__users=user,
            uuid=section_uuid,
        ).get()
    except Section.DoesNotExist:
        return None
