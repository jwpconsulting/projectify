# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
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
# Generated by Django 4.2.7 on 2023-12-25 05:13
"""Make User a BaseModel."""

import django.utils.timezone
from django.db import migrations

import django_extensions.db.fields


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("user", "0010_user_privacy_policy_agreed_user_tos_agreed"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={"get_latest_by": "modified"},
        ),
        migrations.AddField(
            model_name="user",
            name="created",
            field=django_extensions.db.fields.CreationDateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="created",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="modified",
            field=django_extensions.db.fields.ModificationDateTimeField(
                auto_now=True, verbose_name="modified"
            ),
        ),
    ]
