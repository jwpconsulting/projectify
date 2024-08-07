# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2021, 2022 JWP Consulting GK
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
"""Create workspace user invite."""
# Generated by Django 4.0.2 on 2022-03-09 07:38

import django.db.models.deletion
from django.db import (
    migrations,
    models,
)

import projectify.lib.models


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("user", "0008_userinvite"),
        ("workspace", "0023_alter_label_color"),
    ]

    operations = [
        migrations.CreateModel(
            name="WorkspaceUserInvite",
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
                    "created",
                    projectify.lib.models.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    projectify.lib.models.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "user_invite",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.userinvite",
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
                "unique_together": {("user_invite", "workspace")},
            },
        ),
    ]
