# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Add minimized_project_list field to TeamMember model."""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Run the migration."""

    dependencies = [
        ("workspace", "0069_userpreferences"),
    ]

    operations = [
        migrations.AddField(
            model_name="teammember",
            name="minimized_project_list",
            field=models.BooleanField(
                default=False,
                help_text="Whether this team member has minimized the project list in this workspace",
            ),
        ),
    ]
