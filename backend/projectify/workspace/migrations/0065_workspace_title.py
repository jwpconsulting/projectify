# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023-2024 JWP Consulting GK
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
"""Change workspace title to not allow for url like strings."""
# Generated by Django 5.0.3 on 2024-04-09 06:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("workspace", "0064_alter_label_color"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="workspace",
            constraint=models.CheckConstraint(
                check=models.Q(("title__regex", "^([.:]\\s|[^.:])*[.:]?$")),
                name="title",
                violation_error_message="Workspace title can only contain '.' or ':' if followed by whitespace or if located at the end.",
            ),
        ),
    ]