# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Selectors for the workspace app Label model."""

import logging
from typing import Optional
from uuid import UUID

from django.db.models import Case, Prefetch, QuerySet, Value, When
from django.utils.encoding import force_str

from projectify.user.models import User

from ..models.const import COLOR_MAP
from ..models.label import Label
from ..models.project import Project

logger = logging.getLogger(__name__)


def labels_annotate_with_colors(label_qs: QuerySet[Label]) -> QuerySet[Label]:
    """Annotate labels with bg_class and border_class based on COLOR_MAP."""
    bg_cases = [
        When(color=i, then=Value(color_info["bg_class"]))
        for i, color_info in COLOR_MAP.items()
    ]
    border_cases = [
        When(color=i, then=Value(color_info["border_class"]))
        for i, color_info in COLOR_MAP.items()
    ]
    text_cases = [
        When(color=i, then=Value(color_info["text_class"]))
        for i, color_info in COLOR_MAP.items()
    ]
    name_cases = [
        When(color=i, then=Value(force_str(color_info["name"])))
        for i, color_info in COLOR_MAP.items()
    ]

    return label_qs.annotate(
        bg_class=Case(*bg_cases),
        border_class=Case(*border_cases),
        text_class=Case(*text_cases),
        color_name=Case(*name_cases),
    )


LabelDetailQuerySet = Label.objects.select_related(
    "workspace"
).prefetch_related(
    Prefetch(
        "workspace__project_set",
        queryset=Project.objects.filter(archived__isnull=True),
    ),
)


def label_find_by_label_uuid(
    *,
    label_uuid: UUID,
    who: User,
    qs: Optional[QuerySet[Label]] = None,
) -> Optional[Label]:
    """Find a label by uuid for a given user."""
    if qs is None:
        qs = Label.objects.all()
    qs = qs.filter(uuid=label_uuid, workspace__users=who)
    try:
        return qs.get()
    except Label.DoesNotExist:
        logger.warning("No label for for UUID %s", label_uuid)
        return None
