# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Test dashboard views."""

from django.http import HttpResponseRedirect
from django.test.client import Client
from django.urls import reverse

import pytest
from faker import Faker

from projectify.workspace.models.project import Project
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.services.project import (
    project_archive,
    project_create,
)

pytestmark = pytest.mark.django_db


class TestRedirectToDashboard:
    """Test redirect_to_dashboard view."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("dashboard:dashboard")

    def test_redirect_to_welcome_when_no_workspace(
        self, user_client: Client, resource_url: str
    ) -> None:
        """Test redirect to welcome page when user has no workspaces."""
        response = user_client.get(resource_url)

        assert isinstance(response, HttpResponseRedirect)
        assert response.status_code == 302
        assert response.url == reverse("onboarding:welcome")

    def test_redirect_to_project_when_workspace_has_project(
        self,
        user_client: Client,
        resource_url: str,
        team_member: TeamMember,
        project: Project,
    ) -> None:
        """Test redirect to project detail when workspace has projects."""
        response = user_client.get(resource_url)

        assert isinstance(response, HttpResponseRedirect)
        assert response.status_code == 302
        assert response.url == reverse(
            "dashboard:projects:detail", kwargs={"project_uuid": project.uuid}
        )

    def test_redirect_to_new_project_when_no_projects(
        self,
        user_client: Client,
        resource_url: str,
        workspace: Workspace,
        team_member: TeamMember,
    ) -> None:
        """Test redirect to new project onboarding when workspace has no projects."""
        response = user_client.get(resource_url)

        assert isinstance(response, HttpResponseRedirect)
        assert response.status_code == 302
        assert response.url == reverse(
            "onboarding:new_project", kwargs={"workspace_uuid": workspace.uuid}
        )

    def test_redirect_ignores_archived_projects(
        self,
        user_client: Client,
        resource_url: str,
        workspace: Workspace,
        team_member: TeamMember,
        project: Project,
    ) -> None:
        """Test that archived projects are ignored when checking for projects."""
        project_archive(who=team_member.user, project=project, archived=True)

        response = user_client.get(resource_url)

        assert isinstance(response, HttpResponseRedirect)
        assert response.status_code == 302
        assert response.url == reverse(
            "onboarding:new_project", kwargs={"workspace_uuid": workspace.uuid}
        )

    def test_redirect_to_first_project_when_multiple_projects(
        self,
        user_client: Client,
        resource_url: str,
        workspace: Workspace,
        team_member: TeamMember,
        project: Project,
        faker: Faker,
    ) -> None:
        """Test redirect to second project when workspace has two projects."""
        del project
        new_project = project_create(
            who=team_member.user,
            title=faker.text(),
            description=faker.paragraph(),
            workspace=workspace,
        )

        response = user_client.get(resource_url)

        assert isinstance(response, HttpResponseRedirect)
        assert response.status_code == 302
        assert response.url == reverse(
            "dashboard:projects:detail",
            kwargs={"project_uuid": new_project.uuid},
        )
