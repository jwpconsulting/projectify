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
"""Add UUID fields."""
# Generated by Django 3.2.10 on 2021-12-23 06:34

import uuid

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("workspace", "0009_subtask"),
    ]

    operations = [
        migrations.AddField(
            model_name="subtask",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, unique=True
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, unique=True
            ),
        ),
        migrations.AddField(
            model_name="workspace",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, unique=True
            ),
        ),
        migrations.AddField(
            model_name="workspaceboard",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, unique=True
            ),
        ),
        migrations.AddField(
            model_name="workspaceboardsection",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, unique=True
            ),
        ),
        migrations.AddField(
            model_name="workspaceuser",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, unique=True
            ),
        ),
    ]
