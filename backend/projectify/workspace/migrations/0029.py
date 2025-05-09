# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2023 JWP Consulting GK
"""Unique Constraint for Order on Workspace Board Section and Task."""
# Generated by Django 3.2.12 on 2022-03-17 01:15

import django.db.models.constraints
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("workspace", "0028"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="task",
            constraint=models.UniqueConstraint(
                deferrable=django.db.models.constraints.Deferrable["DEFERRED"],
                fields=("workspace_board_section", "_order"),
                name="unique_task_order",
            ),
        ),
        migrations.AddConstraint(
            model_name="workspaceboardsection",
            constraint=models.UniqueConstraint(
                deferrable=django.db.models.constraints.Deferrable["DEFERRED"],
                fields=("workspace_board", "_order"),
                name="unique_workspace_board_order",
            ),
        ),
    ]
