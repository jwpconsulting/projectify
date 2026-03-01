# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Test project CRUD views."""

import re
from datetime import datetime
from uuid import uuid4

from django.test.client import Client
from django.urls import reverse

import pytest

from pytest_types import DjangoAssertNumQueries

from ...models import Label, Project, Section, Task, TeamMember, Workspace
from ...services.task import task_create

pytestmark = pytest.mark.django_db


class TestProjectDetailView:
    """Test html project detail view."""

    @pytest.fixture
    def resource_url(self, project: Project) -> str:
        """Return URL to this view."""
        return reverse("dashboard:projects:detail", args=(project.uuid,))

    def test_get_project_detail(
        self,
        user_client: Client,
        resource_url: str,
        project: Project,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test GETting the project detail page."""
        # Gone up   from 14 -> 15, since we fetch all workspaces
        # Gone down from 15 -> 14, since we optimized the prefetches
        # Gone down from 14 -> 13, since we select the related workspace
        # Gone down from 13 -> 11, since we prefetch projects
        # Gone down from 11 -> 10, since we don't fetch label values()
        # Gone up   from 10 -> 13, since we update the last visited project
        # Gone up   from 13 -> 15
        # Gone down from 15 -> 14
        # Gone up   from 14 -> 15
        # Gone up   from 15 -> 18
        with django_assert_num_queries(18):
            response = user_client.get(resource_url)
            assert response.status_code == 200
        assert project.title in response.content.decode()
        assert project.workspace.title in response.content.decode()

    def test_project_not_found(
        self,
        user_client: Client,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Ensure that accessing a non-existent project returns 404."""
        url = reverse("dashboard:projects:detail", args=(uuid4(),))
        with django_assert_num_queries(3):
            response = user_client.get(url)
            assert response.status_code == 404

    def test_archived_project_not_found(
        self,
        user_client: Client,
        archived_project: Project,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Ensure that the client can't access archived projects."""
        url = reverse(
            "dashboard:projects:detail", args=(archived_project.uuid,)
        )
        with django_assert_num_queries(3):
            response = user_client.get(url)
            assert response.status_code == 404

    def test_filter_by_team_member(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        other_team_member: TeamMember,
        task: Task,
        other_task: Task,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test filtering tasks by team member."""
        task.assignee = team_member
        task.save()

        other_task.assignee = other_team_member
        other_task.save()

        with django_assert_num_queries(22):
            response = user_client.get(
                resource_url,
                {"filter_by_team_member": [str(team_member.uuid)]},
            )
            assert response.status_code == 200

        assert task.title in response.content.decode()
        assert other_task.title not in response.content.decode()

    def test_filter_by_unassigned_tasks(
        self,
        user_client: Client,
        resource_url: str,
        task: Task,
        team_member: TeamMember,
        other_task: Task,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test filtering for unassigned tasks."""
        task.assignee = team_member
        task.save()

        with django_assert_num_queries(20):
            response = user_client.get(
                resource_url, {"filter_by_team_member": [""]}
            )
            assert response.status_code == 200

        assert task.title not in response.content.decode()
        assert other_task.title in response.content.decode()

    def test_filter_by_label(
        self,
        user_client: Client,
        resource_url: str,
        task: Task,
        other_task: Task,
        label: Label,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test filtering tasks by label."""
        task.labels.add(label)

        with django_assert_num_queries(22):
            response = user_client.get(
                resource_url, {"filter_by_label": [str(label.uuid)]}
            )
            assert response.status_code == 200

        assert task.title in response.content.decode()
        assert other_task.title not in response.content.decode()

    def test_filter_by_unlabeled_tasks(
        self,
        user_client: Client,
        resource_url: str,
        task: Task,
        other_task: Task,
        label: Label,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test filtering for unlabeled tasks."""
        task.labels.add(label)

        with django_assert_num_queries(20):
            response = user_client.get(resource_url, {"filter_by_label": [""]})
            assert response.status_code == 200

        assert task.title not in response.content.decode()
        assert other_task.title in response.content.decode()

    def test_filter_by_task_search_query(
        self,
        user_client: Client,
        resource_url: str,
        task: Task,
        other_task: Task,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test filtering tasks by search query."""
        task.title = "Important bug fix"
        task.save()

        other_task.title = "Feature request"
        other_task.save()

        with django_assert_num_queries(20):
            response = user_client.get(
                resource_url, {"task_search_query": "bug"}
            )
            assert response.status_code == 200

        assert task.title in response.content.decode()
        assert other_task.title not in response.content.decode()


class TestProjectDetailViewActions:
    """Test project detail view actions."""

    @pytest.fixture
    def resource_url(self, project: Project) -> str:
        """Return URL to this view."""
        return reverse("dashboard:projects:detail", args=(project.uuid,))

    def test_move_task_up_down(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        task: Task,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test moving tasks up and down within a section."""
        section = task.section
        task2 = task_create(
            who=team_member.user, section=task.section, title="Second task"
        )
        assert list(section.task_set.values_list("pk", flat=True)) == [
            task.pk,
            task2.pk,
        ]

        # Move task2 up (should swap positions)
        with django_assert_num_queries(32):
            response = user_client.post(
                resource_url,
                {
                    "action": "move_task",
                    "task_uuid": str(task2.uuid),
                    "direction": "up",
                },
            )
            assert response.status_code == 200
        assert list(section.task_set.values_list("pk", flat=True)) == [
            task2.pk,
            task.pk,
        ]

        # Move task1 up (should swap back)
        with django_assert_num_queries(32):
            response = user_client.post(
                resource_url,
                {
                    "action": "move_task",
                    "task_uuid": str(task.uuid),
                    "direction": "up",
                },
            )
            assert response.status_code == 200
        assert list(section.task_set.values_list("pk", flat=True)) == [
            task.pk,
            task2.pk,
        ]

    def test_move_task_form_validation(
        self, user_client: Client, resource_url: str, task: Task
    ) -> None:
        """Test form validation."""
        response = user_client.post(
            resource_url,
            {
                "action": "move_task",
                "task_uuid": str(task.uuid),
                "direction": "inv",
            },
        )
        assert response.status_code == 400
        response = user_client.post(
            resource_url,
            {
                "action": "move_task",
                "task_uuid": str(uuid4()),
                "direction": "up",
            },
        )
        assert response.status_code == 400

    def test_mark_task_done(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        task: Task,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test marking a task as done and then not done."""
        assert task.done is None
        t_uid = str(task.uuid)
        data = {"action": "mark_task_done", "task_uuid": t_uid, "done": "true"}
        with django_assert_num_queries(24):
            response = user_client.post(resource_url, data)
            assert response.status_code == 200
        task.refresh_from_db()
        assert task.done is not None

        data = {
            "action": "mark_task_done",
            "task_uuid": t_uid,
            "done": "false",
        }
        with django_assert_num_queries(24):
            response = user_client.post(resource_url, data)
            assert response.status_code == 200
        task.refresh_from_db()
        assert task.done is None

    def test_mark_task_done_form_validation(
        self, user_client: Client, resource_url: str
    ) -> None:
        """Test form validation for mark task done action."""
        d = {"action": "mark_task_done"}
        response = user_client.post(
            resource_url, {**d, "task_uuid": str(uuid4()), "done": "true"}
        )
        assert response.status_code == 400
        response = user_client.post(
            resource_url, {**d, "action": "mark_task_done", "done": "true"}
        )
        assert response.status_code == 400


class TestProjectCreateView:
    """Test html project create view."""

    @pytest.fixture
    def resource_url(self, workspace: Workspace) -> str:
        """Return URL to this view."""
        return reverse(
            "dashboard:workspaces:create-project", args=(workspace.uuid,)
        )

    def test_get(
        self, user_client: Client, resource_url: str, team_member: TeamMember
    ) -> None:
        """Test getting this page."""
        response = user_client.get(resource_url)
        assert response.status_code == 200

    def test_create_project_success(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test successfully creating a project."""
        initial_project_count = Project.objects.count()
        with django_assert_num_queries(6):
            response = user_client.post(
                resource_url, {"title": "New Test Project"}
            )
            assert response.status_code == 302

        assert Project.objects.count() == initial_project_count + 1

    def test_create_project_invalid_form(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
    ) -> None:
        """Test form validation with invalid data."""
        initial_project_count = Project.objects.count()
        response = user_client.post(resource_url, {})
        assert response.status_code == 400
        assert Project.objects.count() == initial_project_count

    def test_workspace_not_found(
        self,
        user_client: Client,
        team_member: TeamMember,
    ) -> None:
        """Test accessing project creation for non-existent workspace."""
        url = reverse("dashboard:workspaces:create-project", args=(uuid4(),))
        response = user_client.get(url)
        assert response.status_code == 404

    def test_unauthorized_workspace_access(
        self,
        user_client: Client,
        unrelated_workspace: Workspace,
    ) -> None:
        """Test that users can't create projects in other workspaces."""
        url = reverse(
            "dashboard:workspaces:create-project",
            args=(unrelated_workspace.uuid,),
        )
        response = user_client.get(url)
        assert response.status_code == 404


class TestProjectUpdateView:
    """Test html project update view."""

    @pytest.fixture
    def resource_url(self, project: Project) -> str:
        """Return URL to this view."""
        return reverse("dashboard:projects:update", args=(project.uuid,))

    def test_get_project_update(
        self,
        user_client: Client,
        resource_url: str,
        project: Project,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test GETting the project update page."""
        with django_assert_num_queries(8):
            response = user_client.get(resource_url)
            assert response.status_code == 200
            assert project.title.encode() in response.content

    def test_post_success(
        self,
        user_client: Client,
        resource_url: str,
        project: Project,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test successfully updating a project."""
        updated_title = "Updated Project Title"

        with django_assert_num_queries(9):
            response = user_client.post(
                resource_url,
                {"title": updated_title},
            )
            assert response.status_code == 302

        project.refresh_from_db()
        assert project.title == updated_title

    def test_update_project_invalid_form(
        self,
        user_client: Client,
        resource_url: str,
        project: Project,
        team_member: TeamMember,
    ) -> None:
        """Test form validation with invalid data."""
        original_title = project.title
        response = user_client.post(resource_url, {"title": ""})
        assert response.status_code == 400

        project.refresh_from_db()
        assert project.title == original_title, "Shouldn't change"

    def test_project_not_found(
        self,
        user_client: Client,
        team_member: TeamMember,
    ) -> None:
        """Ensure that updating a non-existent project returns 404."""
        url = reverse("dashboard:projects:update", args=(uuid4(),))
        response = user_client.get(url)
        assert response.status_code == 404

    def test_archived_project_not_found(
        self,
        user_client: Client,
        archived_project: Project,
        team_member: TeamMember,
    ) -> None:
        """Ensure that the client can't update archived projects."""
        url = reverse(
            "dashboard:projects:update", args=(archived_project.uuid,)
        )
        response = user_client.get(url)
        assert response.status_code == 404

    def test_unauthorized_project_access(
        self,
        user_client: Client,
        unrelated_project: Project,
    ) -> None:
        """Test that users can't update projects they don't have access to."""
        url = reverse(
            "dashboard:projects:update", args=(unrelated_project.uuid,)
        )
        response = user_client.get(url)
        assert response.status_code == 404


class TestProjectArchiveView:
    """Test html project archive view."""

    @pytest.fixture
    def resource_url(self, project: Project) -> str:
        """Return URL to this view."""
        return reverse("dashboard:projects:archive", args=(project.uuid,))

    def test_post_archive_project(
        self,
        user_client: Client,
        resource_url: str,
        project: Project,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test successfully archiving a project via HTMX."""
        assert not project.archived
        with django_assert_num_queries(6):
            response = user_client.post(resource_url)
            assert response.status_code == 200
        project.refresh_from_db()
        assert project.archived

    def test_project_not_found(
        self,
        user_client: Client,
        team_member: TeamMember,
    ) -> None:
        """Test archiving a non-existent project returns 404."""
        url = reverse("dashboard:projects:archive", args=(uuid4(),))
        response = user_client.post(url)
        assert response.status_code == 404

    def test_already_archived_project_not_found(
        self,
        user_client: Client,
        archived_project: Project,
        team_member: TeamMember,
    ) -> None:
        """Test that already archived projects can't be archived again."""
        url = reverse(
            "dashboard:projects:archive", args=(archived_project.uuid,)
        )
        response = user_client.post(url)
        assert response.status_code == 404

    def test_unauthorized_project_access(
        self,
        user_client: Client,
        unrelated_project: Project,
    ) -> None:
        """Test that users can't archive projects they don't have access to."""
        url = reverse(
            "dashboard:projects:archive", args=(unrelated_project.uuid,)
        )
        response = user_client.post(url)
        assert response.status_code == 404


class TestProjectRecoverView:
    """Test html project recover view."""

    @pytest.fixture
    def resource_url(self, archived_project: Project) -> str:
        """Return URL to this view."""
        return reverse(
            "dashboard:projects:recover", args=(archived_project.uuid,)
        )

    def test_post_recover_project(
        self,
        user_client: Client,
        resource_url: str,
        archived_project: Project,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test successfully recovering an archived project via HTMX."""
        assert archived_project.archived

        with django_assert_num_queries(6):
            response = user_client.post(resource_url)
            assert response.status_code == 200

        archived_project.refresh_from_db()
        assert not archived_project.archived

    def test_get_method_not_allowed(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
    ) -> None:
        """Test that GET requests are not allowed."""
        response = user_client.get(resource_url)
        assert response.status_code == 405

    def test_project_not_found(
        self,
        user_client: Client,
        team_member: TeamMember,
    ) -> None:
        """Test recovering a non-existent project returns 404."""
        url = reverse("dashboard:projects:recover", args=(uuid4(),))
        response = user_client.post(url)
        assert response.status_code == 404

    def test_active_project_not_found(
        self,
        user_client: Client,
        project: Project,
        team_member: TeamMember,
    ) -> None:
        """Test that active (non-archived) projects can't be recovered."""
        url = reverse("dashboard:projects:recover", args=(project.uuid,))
        response = user_client.post(url)
        assert response.status_code == 404

    def test_unauthorized_project_access(
        self,
        user_client: Client,
        unrelated_project: Project,
        now: datetime,
    ) -> None:
        """Test that users can't recover projects they don't have access to."""
        unrelated_project.archived = now
        unrelated_project.save()
        url = reverse(
            "dashboard:projects:recover",
            args=(unrelated_project.uuid,),
        )
        response = user_client.post(url)
        assert response.status_code == 404


class TestProjectDeleteView:
    """Test html project delete view."""

    @pytest.fixture
    def resource_url(self, archived_project: Project) -> str:
        """Return URL to this view."""
        return reverse(
            "dashboard:projects:delete", args=(archived_project.uuid,)
        )

    def test_post_delete_project(
        self,
        user_client: Client,
        resource_url: str,
        archived_project: Project,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test successfully deleting an archived project via HTMX."""
        project_uuid = archived_project.uuid
        assert archived_project.archived
        # Gone from 7 -> 8 since we delete user preferences
        with django_assert_num_queries(8):
            response = user_client.post(resource_url)
            assert response.status_code == 200
        assert not Project.objects.filter(uuid=project_uuid).exists()

    def test_get_method_not_allowed(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
    ) -> None:
        """Test that GET requests are not allowed."""
        response = user_client.get(resource_url)
        assert response.status_code == 405

    def test_project_not_found(
        self,
        user_client: Client,
        team_member: TeamMember,
    ) -> None:
        """Test deleting a non-existent project returns 404."""
        url = reverse("dashboard:projects:delete", args=(uuid4(),))
        response = user_client.post(url)
        assert response.status_code == 404

    def test_active_project_not_found(
        self,
        user_client: Client,
        project: Project,
        team_member: TeamMember,
    ) -> None:
        """Test that active (non-archived) projects can't be deleted."""
        url = reverse("dashboard:projects:delete", args=(project.uuid,))
        response = user_client.post(url)
        assert response.status_code == 404

    def test_unauthorized_project_access(
        self,
        user_client: Client,
        unrelated_project: Project,
        now: datetime,
    ) -> None:
        """Test that users can't delete projects they don't have access to."""
        unrelated_project.archived = now
        unrelated_project.save()
        url = reverse(
            "dashboard:projects:delete",
            args=(unrelated_project.uuid,),
        )
        response = user_client.post(url)
        assert response.status_code == 404


class TestProjectDetailMinimize:
    """Test minimize functionality in project detail view."""

    @pytest.fixture
    def resource_url(self, project: Project) -> str:
        """Return URL to project detail view."""
        return reverse(
            "dashboard:projects:detail",
            args=(project.uuid,),
        )

    @pytest.mark.parametrize(
        "initial_state,post_value,expected_state",
        [
            (False, "true", True),
            (True, "false", False),
        ],
    )
    def test_toggle_team_member_filter(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        initial_state: bool,
        post_value: str,
        expected_state: bool,
    ) -> None:
        """Test toggling the team member filter minimized state."""
        team_member.minimized_team_member_filter = initial_state
        team_member.save()

        response = user_client.post(
            resource_url,
            {
                "action": "minimize_team_member_filter",
                "minimized": post_value,
            },
        )
        assert response.status_code == 200

        team_member.refresh_from_db()
        assert team_member.minimized_team_member_filter is expected_state

    @pytest.mark.parametrize(
        "initial_state,post_value,expected_state",
        [
            (False, "true", True),
            (True, "false", False),
        ],
    )
    def test_toggle_label_filter(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        initial_state: bool,
        post_value: str,
        expected_state: bool,
    ) -> None:
        """Test toggling the label filter minimized state."""
        team_member.minimized_label_filter = initial_state
        team_member.save()

        response = user_client.post(
            resource_url,
            {"action": "minimize_label_filter", "minimized": post_value},
        )
        assert response.status_code == 200

        team_member.refresh_from_db()
        assert team_member.minimized_label_filter is expected_state

    def test_minimize_preserves_get_parameters(
        self,
        user_client: Client,
        team_member: TeamMember,
        resource_url: str,
    ) -> None:
        """Test that GET parameters are preserved after minimize action."""
        response = user_client.post(
            resource_url,
            {
                "action": "minimize_team_member_filter",
                "filter_by_team_member": team_member.uuid,
                "minimized": "true",
            },
        )
        assert response.status_code == 200
        pattern = rf'<input[^>]*name="filter_by_team_member"[^>]*value="{team_member.uuid}"[^>]*checked[^>]*>'
        assert re.search(
            pattern, response.content.decode()
        ), "Team member filter checkbox should be checked"

    @pytest.mark.parametrize(
        "initial_state,form_value,expected_final_state",
        [
            (False, "true", True),  # minimize section
            (True, "false", False),  # expand section
        ],
    )
    def test_section_minimize_toggle(
        self,
        user_client: Client,
        team_member: TeamMember,
        section: Section,
        initial_state: bool,
        form_value: str,
        expected_final_state: bool,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test minimizing and expanding a section."""
        if initial_state:
            section.minimized_by.add(team_member.user)

        assert (
            section.minimized_by.filter(pk=team_member.user.pk).exists()
            == initial_state
        )

        url = reverse(
            "dashboard:projects:detail", args=(section.project.uuid,)
        )

        with django_assert_num_queries(19):
            response = user_client.post(
                url,
                {
                    "action": "minimize_section",
                    "section": str(section.uuid),
                    "minimized": form_value,
                },
            )
            assert response.status_code == 200

        section.refresh_from_db()
        assert (
            section.minimized_by.filter(pk=team_member.user.pk).exists()
            == expected_final_state
        )

    def test_minimize_section_not_found(
        self,
        user_client: Client,
        team_member: TeamMember,
        project: Project,
    ) -> None:
        """Test minimize view with non-existent section."""
        url = reverse("dashboard:projects:detail", args=(project.uuid,))
        response = user_client.post(
            url,
            {
                "action": "minimize_section",
                "section": str(uuid4()),
                "minimized": "true",
            },
        )
        assert response.status_code == 400
