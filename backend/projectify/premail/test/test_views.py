# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2021 JWP Consulting GK
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
"""Test premail views."""
from django.urls import (
    reverse,
)

import pytest


@pytest.mark.django_db
class TestEmailList:
    """Test EmailList."""

    @pytest.fixture
    def resource_url(self):
        """Return URL to this view."""
        return reverse("premail:email-list")

    def test_non_superuser(self, user_client, resource_url):
        """Assert we can't view this while being a normal user."""
        response = user_client.get(resource_url)
        assert response.status_code == 403

    def test_superuser(self, superuser_client, resource_url):
        """Assert we can view this while being a super user."""
        response = superuser_client.get(resource_url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestEmailPreview:
    """Test EmailPreview."""

    @pytest.fixture
    def resource_url(self):
        """Return URL to this view."""
        return reverse("premail:email-preview", kwargs={"slug": "SampleEmail"})

    def test_non_superuser(self, user_client, resource_url):
        """Assert we can't view this while being a normal user."""
        response = user_client.get(resource_url)
        assert response.status_code == 403

    def test_superuser(self, superuser_client, resource_url):
        """Assert we can view this while being a super user."""
        response = superuser_client.get(resource_url)
        assert response.status_code == 200
