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
"""Make task.workspace non-nullable."""
# Generated by Django 4.0.4 on 2022-06-18 05:47

import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("workspace", "0037_alter_task_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="workspace",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="workspace.workspace",
            ),
        ),
    ]
