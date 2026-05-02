# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021-2024,2026 JWP Consulting GK
"""Test workspace models."""

from django.core.exceptions import ValidationError

import pytest

from ..models import Task, Workspace

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


class TestTask:
    """Test Task."""

    def test_ws_assign(
        self, task: Task, unrelated_workspace: Workspace
    ) -> None:
        """Test that save checks the workspace."""
        # Changed from db.InternalError, see above in test_save_no_number
        task.workspace = unrelated_workspace
        with pytest.raises(ValidationError):
            task.save()
