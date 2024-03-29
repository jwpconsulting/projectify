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
"""Add deadline to workspace."""
# Generated by Django 4.0.2 on 2022-03-04 03:47

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("workspace", "0017_workspace_picture"),
    ]

    operations = [
        migrations.AddField(
            model_name="workspaceboard",
            name="deadline",
            field=models.DateTimeField(
                blank=True, help_text="Workspace board's deadline", null=True
            ),
        ),
    ]
