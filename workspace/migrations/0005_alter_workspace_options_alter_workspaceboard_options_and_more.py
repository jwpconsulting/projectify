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
"""Add title and description."""
# Generated by Django 4.0 on 2021-12-15 07:06

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        (
            "workspace",
            "0004_alter_workspace_options_alter_"
            "workspaceboard_options_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="workspace",
            options={},
        ),
        migrations.AlterModelOptions(
            name="workspaceboard",
            options={},
        ),
        migrations.AddField(
            model_name="workspace",
            name="description",
            field=models.TextField(
                blank=True, null=True, verbose_name="description"
            ),
        ),
        migrations.AddField(
            model_name="workspace",
            name="title",
            field=models.CharField(
                default="", max_length=255, verbose_name="title"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="workspaceboard",
            name="description",
            field=models.TextField(
                blank=True, null=True, verbose_name="description"
            ),
        ),
        migrations.AddField(
            model_name="workspaceboard",
            name="title",
            field=models.CharField(
                default="", max_length=255, verbose_name="title"
            ),
            preserve_default=False,
        ),
    ]
