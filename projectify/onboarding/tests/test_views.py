# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Test onboarding views."""

from uuid import uuid4

from django.test.client import Client
from django.urls import reverse

import pytest

from projectify.user.models import User
from projectify.workspace.models.label import Label
from projectify.workspace.models.project import Project
from projectify.workspace.models.task import Task
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.models.workspace import Workspace
from pytest_types import DjangoAssertNumQueries

pytestmark = pytest.mark.django_db


class MixinForTests:
    """Test what happens when you're unauthenticated."""

    def test_unauthenticated(self, client: Client, resource_url: str) -> None:
        """Assert that it redirects unauthenticated users."""
        assert client.get(resource_url).status_code == 302

    def test_get_page(self, user_client: Client, resource_url: str) -> None:
        """Get the page."""
        assert user_client.get(resource_url).status_code == 200


class TestWelcome(MixinForTests):
    """Test welcome view."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL for this view."""
        return reverse("onboarding:welcome")


class TestAboutYou(MixinForTests):
    """Test about you view."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("onboarding:about_you")

    def test_post_about_you(
        self,
        user_client: Client,
        resource_url: str,
        user: User,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test setting a name."""
        with django_assert_num_queries(10):
            assert (
                user_client.post(
                    resource_url, {"preferred_name": "Test User"}
                ).status_code
                == 302
            )
        user.refresh_from_db()
        assert user.preferred_name == "Test User"

    def test_post_about_you_invalid(
        self, user_client: Client, resource_url: str
    ) -> None:
        """Test posting a very long name."""
        assert (
            user_client.post(
                resource_url, {"preferred_name": "l" * 999}
            ).status_code
            == 400
        )


class TestNewWorkspace(MixinForTests):
    """Test new workspace view."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to new workspace page."""
        return reverse("onboarding:new_workspace")

    def test_workspace_creation(
        self,
        user_client: Client,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Create a new workspace."""
        with django_assert_num_queries(9):
            assert (
                user_client.post(
                    resource_url, {"title": "Woof woof"}
                ).status_code
                == 302
            )
        Workspace.objects.get(title="Woof woof")

    def test_post_new_workspace_invalid(
        self, user_client: Client, resource_url: str
    ) -> None:
        """Test form validation."""
        assert user_client.post(resource_url, {"title": ""}).status_code == 400


class TestNewProject(MixinForTests):
    """Test new project view."""

    @pytest.fixture
    def resource_url(self, workspace: Workspace) -> str:
        """Return URL to this view."""
        return reverse("onboarding:new_project", args=[str(workspace.uuid)])

    def test_project_creation(
        self,
        user_client: Client,
        resource_url: str,
        workspace: Workspace,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test creating a new project."""
        with django_assert_num_queries(10):
            response = user_client.post(resource_url, {"title": "BarFoo"})
            assert response.status_code == 302
        project = Project.objects.get(title="BarFoo")
        assert project.workspace == workspace

    def test_form_validation(
        self, user_client: Client, resource_url: str
    ) -> None:
        """Test creating a project with an empty name."""
        response = user_client.post(resource_url, {"title": ""})
        assert response.status_code == 400

    def test_workspace_not_found(self, user_client: Client) -> None:
        """Test accessing this page for a missing workspace."""
        assert (
            user_client.get(
                reverse("onboarding:new_project", args=[str(uuid4())])
            ).status_code
            == 404
        )

    def test_unauthorized_access(
        self, user_client: Client, unrelated_workspace: Workspace
    ) -> None:
        """Try accessing an unrelated workspace."""
        assert (
            user_client.get(
                reverse(
                    "onboarding:new_project",
                    args=[str(unrelated_workspace.uuid)],
                )
            ).status_code
            == 404
        )


class TestNewTask(MixinForTests):
    """Test new task view."""

    @pytest.fixture
    def resource_url(self, project: Project) -> str:
        """Return URL to this view."""
        return reverse("onboarding:new_task", args=[str(project.uuid)])

    def test_post_new_task(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Create a new task."""
        with django_assert_num_queries(27):
            assert (
                user_client.post(
                    resource_url, {"title": "Test Task"}
                ).status_code
                == 302
            )
        assert team_member.task_set.get() == Task.objects.get()

    def test_form_validation(
        self, user_client: Client, resource_url: str
    ) -> None:
        """Test form validation."""
        assert user_client.post(resource_url, {"title": ""}).status_code == 400

    def test_not_found(self, user_client: Client) -> None:
        """Test not found handling."""
        assert (
            user_client.get(
                reverse("onboarding:new_task", args=[str(uuid4())])
            ).status_code
            == 404
        )

    def test_unauthorized(
        self, user_client: Client, unrelated_project: Project
    ) -> None:
        """Test access control."""
        assert (
            user_client.get(
                reverse(
                    "onboarding:new_task", args=[str(unrelated_project.uuid)]
                )
            ).status_code
            == 404
        )


class TestNewLabel(MixinForTests):
    """Test new label view."""

    @pytest.fixture
    def resource_url(self, other_task: Task) -> str:
        """Return URL to this view."""
        return reverse("onboarding:new_label", args=[str(other_task.uuid)])

    def test_post_new_label(
        self,
        user_client: Client,
        resource_url: str,
        other_task: Task,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test POSTing to new label page."""
        with django_assert_num_queries(26):
            assert (
                user_client.post(
                    resource_url, {"name": "BarkWoof"}
                ).status_code
                == 302
            )
        assert Label.objects.get() in other_task.labels.all()

    def test_form_validation(
        self, user_client: Client, resource_url: str
    ) -> None:
        """Test what happens if we pass in an empty label."""
        assert user_client.post(resource_url, {"name": ""}).status_code == 400

    def test_label_conflict(
        self, user_client: Client, resource_url: str
    ) -> None:
        """Test what happens if we pass in an empty label."""
        assert user_client.post(resource_url, {"name": "T"}).status_code == 302
        assert user_client.post(resource_url, {"name": "T"}).status_code == 400

    def test_task_not_found(self, user_client: Client) -> None:
        """Test not found handling."""
        assert (
            user_client.get(
                reverse("onboarding:new_label", args=[str(uuid4())])
            ).status_code
            == 404
        )

    def test_authorization(
        self, user_client: Client, unrelated_task: Task
    ) -> None:
        """Test that we can't work with unrelated tasks."""
        assert (
            user_client.get(
                reverse(
                    "onboarding:new_label", args=[str(unrelated_task.uuid)]
                )
            ).status_code
            == 404
        )


class TestAssignTask(MixinForTests):
    """Test assign task view."""

    @pytest.fixture
    def resource_url(self, task: Task) -> str:
        """Return URL to this view."""
        return reverse("onboarding:assign_task", args=[str(task.uuid)])

    def test_task_not_found(self, user_client: Client) -> None:
        """Test accessing this page for a missing task."""
        assert (
            user_client.get(
                reverse("onboarding:assign_task", args=[str(uuid4())])
            ).status_code
            == 404
        )

    def test_authorization(
        self, user_client: Client, unrelated_task: Task
    ) -> None:
        """Test authorization."""
        assert (
            user_client.get(
                reverse(
                    "onboarding:assign_task", args=[str(unrelated_task.uuid)]
                )
            ).status_code
            == 404
        )
