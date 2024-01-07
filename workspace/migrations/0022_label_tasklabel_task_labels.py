# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022 JWP Consulting GK
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
"""Add label support."""
# Generated by Django 4.0.2 on 2022-03-07 06:00

import uuid

import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("workspace", "0021_alter_workspaceboardsection_workspace_board"),
    ]

    operations = [
        migrations.CreateModel(
            name="Label",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("color", models.CharField(max_length=64)),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                (
                    "workspace",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="workspace.workspace",
                    ),
                ),
            ],
            options={
                "unique_together": {("workspace", "name")},
            },
        ),
        migrations.CreateModel(
            name="TaskLabel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "label",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="workspace.label",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="workspace.task",
                    ),
                ),
            ],
            options={
                "unique_together": {("task", "label")},
            },
        ),
        migrations.AddField(
            model_name="task",
            name="labels",
            field=models.ManyToManyField(
                through="workspace.TaskLabel", to="workspace.Label"
            ),
        ),
    ]
