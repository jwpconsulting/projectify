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
"""Add ordering to workspace board section."""
# Generated by Django 4.0 on 2021-12-16 04:23

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("workspace", "0006_workspaceboardsection"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="workspaceboardsection",
            options={"ordering": ("workspace_board", "order")},
        ),
        migrations.AddField(
            model_name="workspaceboardsection",
            name="order",
            field=models.PositiveIntegerField(
                db_index=True, default=0, editable=False, verbose_name="order"
            ),
            preserve_default=False,
        ),
    ]
