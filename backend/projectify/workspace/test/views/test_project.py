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
"""Test project CRUD views."""
from unittest.mock import ANY

from django.urls import reverse
from django.utils.timezone import now

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from projectify.workspace.models import TaskLabel
from projectify.workspace.models.project import Project
from projectify.workspace.models.section import Section
from projectify.workspace.models.sub_task import SubTask
from projectify.workspace.models.task import Task
from projectify.workspace.models.team_member import TeamMember
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.selectors.project import (
    project_find_by_workspace_uuid,
)
from projectify.workspace.services.project import project_archive
from projectify.workspace.services.sub_task import sub_task_create
from pytest_types import DjangoAssertNumQueries


# Create
@pytest.mark.django_db
class TestProjectCreate:
    """Test project creation."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("workspace:projects:create")

    def test_authenticated(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        workspace: Workspace,
        # Make sure that we are part of that workspace
        team_member: TeamMember,
    ) -> None:
        """Assert that we can create a new project."""
        del team_member
        with django_assert_num_queries(4):
            response = rest_user_client.post(
                resource_url,
                {
                    "title": "New project, who dis??",
                    "workspace_uuid": str(workspace.uuid),
                },
            )
        assert response.status_code == 201
        assert Project.objects.count() == 1
        project = Project.objects.get()
        assert project.title == "New project, who dis??"


# Read + Update + Delete
@pytest.mark.django_db
class TestProjectReadUpdateDelete:
    """Test ProjectReadUpdateDelete view."""

    @pytest.fixture
    def resource_url(self, project: Project) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:projects:read-update-delete",
            args=(project.uuid,),
        )

    def test_getting(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        project: Project,
        team_member: TeamMember,
        workspace: Workspace,
        task: Task,
        section: Section,
        sub_task: SubTask,
        other_task: Task,
        task_label: TaskLabel,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Assert we can post to this view this while being logged in."""
        sub_task.done = True
        sub_task.save()
        del task_label
        sub_task_create(
            who=team_member.user, task=task, done=False, title="other sub task"
        )
        # Make sure section -> task -> team_member -> user is resolved
        task.assignee = team_member
        task.save()
        # Gone up from 7 -> 12 since we prefetch workspace details too
        with django_assert_num_queries(11):
            response = rest_user_client.get(resource_url)
            assert response.status_code == 200, response.data
        assert response.data == {
            "title": project.title,
            "description": project.description,
            "archived": None,
            "uuid": str(project.uuid),
            "sections": [
                {
                    "uuid": ANY,
                    "_order": 0,
                    "title": section.title,
                    "description": section.description,
                    "tasks": [
                        {
                            "assignee": ANY,
                            "description": other_task.description,
                            "due_date": ANY,
                            "labels": ANY,
                            "number": other_task.number,
                            "sub_task_progress": None,
                            "title": other_task.title,
                            "uuid": ANY,
                        },
                        {
                            "assignee": ANY,
                            "description": task.description,
                            "due_date": ANY,
                            "labels": [ANY],
                            "number": task.number,
                            "sub_task_progress": 0.5,
                            "title": task.title,
                            "uuid": ANY,
                        },
                    ],
                },
            ],
            "workspace": {
                "created": ANY,
                "modified": ANY,
                "uuid": ANY,
                "picture": ANY,
                "title": workspace.title,
                "description": workspace.description,
                "team_members": ANY,
                "team_member_invites": [],
                "projects": ANY,
                "labels": ANY,
                "quota": ANY,
            },
        }
        project_archive(
            who=team_member.user,
            project=project,
            archived=True,
        )

        # When we archive the board, it will return 404
        with django_assert_num_queries(1):
            response = rest_user_client.get(resource_url)
            assert response.status_code == 404, response.content

    def test_updating(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        team_member: TeamMember,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test updating a ws board."""
        del team_member
        with django_assert_num_queries(4):
            response = rest_user_client.put(
                resource_url,
                data={
                    "title": "Project 1337",
                    "description": "This is Project 1337",
                    "due_date": now(),
                },
                format="json",
            )
            assert response.status_code == status.HTTP_200_OK, response.data

    def test_deleting(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        team_member: TeamMember,
        project: Project,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test updating a ws board."""
        # Can't find it, when not archived
        response = rest_user_client.delete(resource_url)
        assert response.status_code == 404, response.content

        project_archive(
            project=project,
            who=team_member.user,
            archived=True,
        )

        with django_assert_num_queries(5):
            response = rest_user_client.delete(resource_url)
            assert (
                response.status_code == status.HTTP_204_NO_CONTENT
            ), response.data


# Read (list)
@pytest.mark.django_db
class TestProjectsArchivedList:
    """Test ProjectsArchived list."""

    @pytest.fixture
    def resource_url(self, workspace: Workspace) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:workspaces:archived-projects",
            args=(workspace.uuid,),
        )

    def test_authenticated(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        team_member: TeamMember,
        # In total 2 projects, but only one shall be returned
        project: Project,
        archived_project: Project,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Assert we can GET this view this while being logged in."""
        del team_member
        del project
        with django_assert_num_queries(2):
            response = rest_user_client.get(resource_url)
            assert response.status_code == 200, response.content
        assert len(response.data) == 1
        assert response.data[0]["uuid"] == str(archived_project.uuid)


# RPC
@pytest.mark.django_db
class TestProjectArchive:
    """Test project archival."""

    @pytest.fixture
    def resource_url(self, project: Project) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:projects:archive",
            args=(str(project.uuid),),
        )

    def test_archiving_and_unarchiving(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        workspace: Workspace,
        team_member: TeamMember,
    ) -> None:
        """Test archiving a board and then unarchiving it."""
        count = len(
            project_find_by_workspace_uuid(
                who=team_member.user,
                workspace_uuid=workspace.uuid,
                archived=False,
            )
        )
        with django_assert_num_queries(4):
            response = rest_user_client.post(
                resource_url,
                data={"archived": True},
            )
            assert response.status_code == 204, response.data
        assert (
            count
            == len(
                project_find_by_workspace_uuid(
                    who=team_member.user,
                    workspace_uuid=workspace.uuid,
                    archived=False,
                )
            )
            + 1
        )
        with django_assert_num_queries(4):
            response = rest_user_client.post(
                resource_url,
                data={"archived": False},
            )
            assert response.status_code == 204, response.data
        assert count == len(
            project_find_by_workspace_uuid(
                who=team_member.user,
                workspace_uuid=workspace.uuid,
                archived=False,
            )
        )
