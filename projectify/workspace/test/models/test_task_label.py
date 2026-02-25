# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Test TaskLabel model."""

import pytest

from ... import models


@pytest.mark.django_db
class TestTaskLabel:
    """Test TaskLabel model."""

    def test_factory(
        self,
        task_label: models.TaskLabel,
        task: models.Task,
        label: models.Label,
    ) -> None:
        """Test factory."""
        assert task_label.task == task
        assert task_label.label == label
