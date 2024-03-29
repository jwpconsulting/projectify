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
"""Add assignee field to Task."""
# Generated by Django 3.2.11 on 2022-02-08 02:21

import django.db.models.deletion
from django.conf import (
    settings,
)
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("workspace", "0012_auto_20220128_1034"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="assignee",
            field=models.ForeignKey(
                blank=True,
                help_text="User this task is assigned to.",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
