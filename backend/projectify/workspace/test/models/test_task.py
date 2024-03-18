# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Test task model and manager."""
from django import (
    db,
)
from django.contrib.auth.models import (
    AbstractUser,
)

import pytest

from projectify.workspace.models.label import Label
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.services.label import label_create

from ... import (
    models,
)


@pytest.mark.django_db
class TestTaskManager:
    """Test TaskManager."""

    def test_filter_by_section_pks(
        self,
        section: models.Section,
        task: models.Task,
    ) -> None:
        """Test filter_by_section_pks."""
        qs = models.Task.objects.filter_by_section_pks(
            [section.pk],
        )
        assert list(qs) == [task]


@pytest.mark.django_db
class TestTask:
    """Test Task."""

    def test_factory(
        self,
        section: models.Section,
        team_member: models.TeamMember,
        task: models.Task,
        user: AbstractUser,
    ) -> None:
        """Test that section is assigned correctly."""
        assert task.section == section
        assert task.due_date is not None

    def test_assign_to(
        self,
        workspace: models.Workspace,
        task: models.Task,
        other_team_member: models.TeamMember,
    ) -> None:
        """Test assigning to a different workspace's user."""
        task.assign_to(other_team_member)
        assert task.assignee == other_team_member

    def test_assign_then_delete_user(
        self, task: models.Task, team_member: models.TeamMember
    ) -> None:
        """Assert that nothing happens to the task if the user is gone."""
        task.assign_to(team_member)
        team_member.user.delete()
        task.refresh_from_db()
        assert task.assignee is None

    def test_assign_outside_of_workspace(
        self,
        workspace: models.Workspace,
        task: models.Task,
        unrelated_team_member: models.TeamMember,
    ) -> None:
        """Test assigning to a different workspace's user."""
        # This time do not create a team_member
        with pytest.raises(models.TeamMember.DoesNotExist):
            task.assign_to(unrelated_team_member)

    def test_assign_none(
        self,
        workspace: models.Workspace,
        task: models.Task,
        team_member: models.TeamMember,
    ) -> None:
        """Test assigning to no user."""
        task.assign_to(team_member)
        task.assign_to(None)
        task.refresh_from_db()
        assert task.assignee is None

    def test_assign_remove_team_member(
        self,
        user: AbstractUser,
        workspace: models.Workspace,
        team_member: models.TeamMember,
        task: models.Task,
    ) -> None:
        """Test what happens if a team member is removed."""
        task.assignee = team_member
        task.save()
        workspace.remove_user(user)
        task.refresh_from_db()
        assert task.assignee is None

    def test_get_next_section(
        self,
        project: models.Project,
        task: models.Task,
        other_section: models.Section,
    ) -> None:
        """Test getting the next section."""
        assert task.get_next_section() == other_section

    def test_get_next_section_no_next_section(
        self, project: models.Project, task: models.Task
    ) -> None:
        """Test getting the next section when there is none."""
        with pytest.raises(models.Section.DoesNotExist):
            task.get_next_section()

    def test_set_labels(
        self,
        workspace: Workspace,
        task: models.Task,
        labels: list[Label],
        team_member: TeamMember,
        unrelated_workspace: Workspace,
        unrelated_team_member: TeamMember,
    ) -> None:
        """Test setting labels."""
        assert task.labels.count() == 0
        a, b, c, d, e = labels
        task.set_labels([a, b])
        assert task.labels.count() == 2
        # The order is inverted since we are not actually sorting by the
        # TaskLabel creation but the default ordering of the label itself
        # Furthermore, we work independently of the service layer, so it is
        # questionable how useful this code is to the application
        # TODO refactor
        assert list(task.labels.values_list("id", flat=True)) == [b.id, a.id]
        task.set_labels([c, d, e])
        assert task.labels.count() == 3
        assert list(task.labels.values_list("id", flat=True)) == [
            e.id,
            d.id,
            c.id,
        ]
        task.set_labels([])
        assert task.labels.count() == 0
        assert list(task.labels.values_list("id", flat=True)) == []

        unrelated = label_create(
            workspace=unrelated_workspace,
            who=unrelated_team_member.user,
            color=0,
            name="don't care",
        )
        task.set_labels([unrelated])
        assert task.labels.count() == 0
        assert list(task.labels.values_list("id", flat=True)) == []

    def test_add_label(self, task: models.Task, label: models.Label) -> None:
        """Test adding a label."""
        assert task.tasklabel_set.count() == 0
        task.add_label(label)
        assert task.tasklabel_set.count() == 1
        # This is idempotent
        task.add_label(label)
        assert task.tasklabel_set.count() == 1

    def test_remove_label(
        self, task: models.Task, label: models.Label
    ) -> None:
        """Test removing a label."""
        task.add_label(label)
        assert task.tasklabel_set.count() == 1
        task.remove_label(label)
        assert task.tasklabel_set.count() == 0
        # This is idempotent
        task.remove_label(label)
        assert task.tasklabel_set.count() == 0

    def test_task_number(
        self, task: models.Task, other_task: models.Task
    ) -> None:
        """Test unique task number."""
        other_task.refresh_from_db()
        task.refresh_from_db()
        assert other_task.number == task.number + 1
        task.workspace.refresh_from_db()
        assert task.workspace.highest_task_number == other_task.number

    def test_save(self, task: models.Task) -> None:
        """Test saving and assert number does not change."""
        num = task.number
        task.save()
        assert task.number == num

    def test_save_no_number(
        self, task: models.Task, workspace: models.Workspace
    ) -> None:
        """Test saving with no number."""
        # With psycopg2 we had an db.InternalError, now with psycopg 3 it
        # became db.ProgrammingError instead
        with pytest.raises(db.ProgrammingError):
            task.number = None  # type: ignore[assignment]
            task.save()
            workspace.refresh_from_db()

    def test_save_different_number(self, task: models.Task) -> None:
        """Test saving with different number."""
        # Changed from db.InternalError, see above in test_save_no_number
        with pytest.raises(db.ProgrammingError):
            task.number = 154785787
            task.save()

    def test_task_workspace_pgtrigger(
        self, task: models.Task, unrelated_workspace: models.Workspace
    ) -> None:
        """Test database trigger for wrong workspace assignment."""
        # Changed from db.InternalError, see above in test_save_no_number
        with pytest.raises(db.ProgrammingError):
            task.workspace = unrelated_workspace
            task.save()
