# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
"""Test label services."""

from django.core.exceptions import ValidationError
from django.db import IntegrityError

import pytest

from ...models import Label, TeamMember, Workspace
from ...services.label import label_create, label_update

pytestmark = pytest.mark.django_db


def test_label_create(workspace: Workspace, team_member: TeamMember) -> None:
    """Test creating a label with valid color."""
    label = label_create(
        workspace=workspace, name="Bug", color=3, who=team_member.user
    )
    assert label.name == "Bug"
    assert label.color == 3
    assert label.workspace == workspace


def test_label_update(team_member: TeamMember, label: Label) -> None:
    """Test updating a label with valid color."""
    updated_label = label_update(
        who=team_member.user, label=label, name="Updated", color=5
    )
    assert updated_label.name == "Updated"
    assert updated_label.color == 5
    assert updated_label.pk == label.pk


def test_label_valid_color_numbers(
    label: Label, team_member: TeamMember
) -> None:
    """Test updating label color numbers."""
    name = label.name
    with pytest.raises((ValidationError, IntegrityError)):
        label_update(who=team_member.user, label=label, name=name, color=-1)

    label_update(who=team_member.user, label=label, name=name, color=0)
    label.refresh_from_db()
    assert label.color == 0

    label_update(who=team_member.user, label=label, name=name, color=7)
    label.refresh_from_db()
    assert label.color == 7

    with pytest.raises((ValidationError, IntegrityError)):
        label_update(who=team_member.user, label=label, name=name, color=8)
