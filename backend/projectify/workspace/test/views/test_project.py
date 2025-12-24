# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Test project CRUD views."""

from datetime import datetime
from unittest.mock import ANY
from uuid import uuid4

from django.test.client import Client
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


# HTML views
@pytest.mark.django_db
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
        with django_assert_num_queries(13):
            response = user_client.get(resource_url)
            assert response.status_code == 200
            assert project.title.encode() in response.content
            assert project.workspace.title.encode() in response.content

    def test_project_not_found(
        self,
        user_client: Client,
        team_member: TeamMember,
    ) -> None:
        """Ensure that accessing a non-existent project returns 404."""
        url = reverse("dashboard:projects:detail", args=(uuid4(),))
        response = user_client.get(url)
        assert response.status_code == 404

    def test_archived_project_not_found(
        self,
        user_client: Client,
        archived_project: Project,
        team_member: TeamMember,
    ) -> None:
        """Ensure that the client can't access archived projects."""
        url = reverse(
            "dashboard:projects:detail", args=(archived_project.uuid,)
        )
        response = user_client.get(url)
        assert response.status_code == 404


@pytest.mark.django_db
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


@pytest.mark.django_db
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
        with django_assert_num_queries(4):
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

        with django_assert_num_queries(5):
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


@pytest.mark.django_db
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


@pytest.mark.django_db
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


@pytest.mark.django_db
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
        with django_assert_num_queries(7):
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
        archived_project: Project,
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
        del archived_project
        sub_task.done = True
        sub_task.save()
        del task_label
        sub_task_create(
            who=team_member.user, task=task, done=False, title="other sub task"
        )
        # Make sure section -> task -> team_member -> user is resolved
        task.assignee = team_member
        task.save()
        # Gone up   from  7 -> 12, since we prefetch workspace details too
        # Gone up   from 11 -> 14, since we fetch workspace quota
        # Gone up   from 14 -> 15, since we match by assignee uuids
        # Gone down from 15 -> 12, since we optimized the prefetch
        # Gone down from 12 -> 11, since we select the related workspace
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
                            "description": task.description,
                            "due_date": ANY,
                            "labels": [ANY],
                            "number": task.number,
                            "sub_task_progress": 0.5,
                            "title": task.title,
                            "uuid": ANY,
                        },
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
                    ],
                },
            ],
            "workspace": {
                "uuid": ANY,
                "picture": ANY,
                "title": workspace.title,
                "description": workspace.description,
                "team_members": ANY,
                "team_member_invites": [],
                "projects": [ANY],
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
