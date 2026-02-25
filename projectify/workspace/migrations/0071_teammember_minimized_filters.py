# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Add minimized_team_member_filter and minimized_label_filter fields to TeamMember model."""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Run the migration."""

    dependencies = [
        ("workspace", "0070_teammember_minimized_project_list"),
    ]

    operations = [
        migrations.AddField(
            model_name="teammember",
            name="minimized_team_member_filter",
            field=models.BooleanField(
                default=False,
                help_text="Whether this team member has minimized the team member filter in this workspace",
            ),
        ),
        migrations.AddField(
            model_name="teammember",
            name="minimized_label_filter",
            field=models.BooleanField(
                default=False,
                help_text="Whether this team member has minimized the label filter in this workspace",
            ),
        ),
    ]
