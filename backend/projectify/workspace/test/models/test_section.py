# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Section model tests."""

import pytest

from ... import models


@pytest.mark.django_db
class TestSection:
    """Test Section."""

    def test_factory(
        self,
        project: models.Project,
        section: models.Section,
    ) -> None:
        """Test section creation works."""
        assert section.project == project
