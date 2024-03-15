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
"""Test section CRUD views."""
from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.urls import (
    reverse,
)

import pytest
from rest_framework import status
from rest_framework.test import (
    APIClient,
)

from projectify.workspace.models import (
    Section,
    TaskLabel,
    Project,
)
from projectify.workspace.models.task import Task
from projectify.workspace.models.workspace import Workspace
from projectify.workspace.models.workspace_user import WorkspaceUser
from pytest_types import (
    DjangoAssertNumQueries,
)


# Create
@pytest.mark.django_db
class TestSectionCreate:
    """Test section creation."""

    @pytest.fixture
    def resource_url(self) -> str:
        """Return URL to this view."""
        return reverse("workspace:sections:create")

    def test_authenticated(
        self,
        user: AbstractBaseUser,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        project: Project,
        # Make sure that we are part of that workspace
        workspace_user: WorkspaceUser,
    ) -> None:
        """Assert that we can create a new project."""
        assert Section.objects.count() == 0
        with django_assert_num_queries(7):
            response = rest_user_client.post(
                resource_url,
                {
                    "title": "New section, who dis??",
                    "project_uuid": str(project.uuid),
                },
            )
        assert response.status_code == 201
        assert Section.objects.count() == 1
        section = Section.objects.get()
        assert section.title == "New section, who dis??"


# Read + Update + Delete
@pytest.mark.django_db
class TestSectionReadUpdateDelete:
    """Test SectionReadUpdateDelete view."""

    @pytest.fixture
    def resource_url(self, section: Section) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:sections:read-update-delete",
            args=(section.uuid,),
        )

    def test_get(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        user: AbstractBaseUser,
        workspace: Workspace,
        workspace_user: WorkspaceUser,
        task: Task,
        other_task: Task,
        task_label: TaskLabel,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Assert we can post to this view this while being logged in."""
        # Make sure task -> workspace_user -> user is resolved
        task.assignee = workspace_user
        task.save()
        with django_assert_num_queries(6):
            response = rest_user_client.get(resource_url)
            assert response.status_code == 200, response.content

    def test_update(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        user: AbstractBaseUser,
        workspace_user: WorkspaceUser,
        django_assert_num_queries: DjangoAssertNumQueries,
        section: Section,
    ) -> None:
        """Test updating a section."""
        with django_assert_num_queries(4):
            response = rest_user_client.put(
                resource_url,
                data={
                    "title": "New title",
                    "description": "New description",
                },
            )
            assert response.status_code == status.HTTP_200_OK, response.data
        assert response.data == {
            "title": "New title",
            "description": "New description",
        }
        section.refresh_from_db()
        assert section.title == "New title"
        assert section.description == "New description"

    def test_delete(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        workspace_user: WorkspaceUser,
        django_assert_num_queries: DjangoAssertNumQueries,
    ) -> None:
        """Test deleting."""
        with django_assert_num_queries(7):
            response = rest_user_client.delete(resource_url)
            assert (
                response.status_code == status.HTTP_204_NO_CONTENT
            ), response.data
        assert Section.objects.count() == 0


# RPC
@pytest.mark.django_db
class TestSectionMove:
    """Test moving a section."""

    @pytest.fixture
    def resource_url(self, section: Section) -> str:
        """Return URL to this view."""
        return reverse(
            "workspace:sections:move",
            args=(str(section.uuid),),
        )

    def test_authenticated_user(
        self,
        rest_user_client: APIClient,
        resource_url: str,
        django_assert_num_queries: DjangoAssertNumQueries,
        section: Section,
        workspace_user: WorkspaceUser,
    ) -> None:
        """Test as an authenticated user."""
        other_section = Section(
            workspace_board=section.project,
            title="test",
        )
        other_section.save()
        assert section._order == 0
        assert other_section._order == 1
        # XXX that's still a whole lot of queries
        # 50% XXX Better now
        with django_assert_num_queries(10):
            response = rest_user_client.post(
                resource_url,
                data={
                    "order": 1,
                },
            )

        assert response.status_code == status.HTTP_200_OK, response.data
        section.refresh_from_db()
        other_section.refresh_from_db()
        assert other_section._order == 0
        assert section._order == 1
