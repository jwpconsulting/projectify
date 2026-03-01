# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2022, 2023 JWP Consulting GK
"""Test workspace models."""

from django import db
from django.core.exceptions import ValidationError

import pytest

from ..models import ChatMessage, Label, Task, TeamMember, Workspace

pytestmark = pytest.mark.django_db


class TestWorkspace:
    """Test Workspace."""

    def test_factory(self, workspace: Workspace) -> None:
        """Assert that the creates."""
        assert workspace

    def test_title_constraint(self, workspace: Workspace) -> None:
        """Assert we can not put URL-like strings in workspace.title."""
        # Copied from projectify/user/test/test_models.py and replaced
        # "user" -> "workspace", "preferred_name" -> "title"
        # Rejected
        workspace.title = "www.google.com"
        with pytest.raises(ValidationError):
            workspace.full_clean()

        workspace.title = "www.google.com."
        with pytest.raises(ValidationError):
            workspace.full_clean()

        workspace.title = "http://localhost"
        with pytest.raises(ValidationError):
            workspace.full_clean()

        # Can't be blank
        workspace.title = ""
        with pytest.raises(ValidationError):
            workspace.full_clean()

        # Allowed
        workspace.title = "John McHurDur Jr."
        workspace.full_clean()

        workspace.title = "http: //localhost"
        workspace.full_clean()

        workspace.title = "Department of: silly walks"
        workspace.full_clean()

        workspace.title = "www. google"
        workspace.full_clean()

        workspace.title = "Foob. Ar"
        workspace.full_clean()


class TestLabel:
    """Test Label model."""

    def test_factory(self, label: Label) -> None:
        """Test factory."""
        assert label.color is not None


class TestChatMessage:
    """Test ChatMessage."""

    def test_factory(
        self, team_member: TeamMember, chat_message: ChatMessage
    ) -> None:
        """Test that chat message belongs to user."""
        assert chat_message.author == team_member


class TestTask:
    """Test Task."""

    def test_task_workspace_pgtrigger(
        self, task: Task, unrelated_workspace: Workspace
    ) -> None:
        """Test database trigger for wrong workspace assignment."""
        # Changed from db.InternalError, see above in test_save_no_number
        with pytest.raises(db.ProgrammingError):
            task.workspace = unrelated_workspace
            task.save()
