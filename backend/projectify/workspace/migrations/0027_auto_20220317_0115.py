# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022 JWP Consulting GK
"""Unique Constraint for Order on Workspace Board Section and Task."""
# Generated by Django 3.2.12 on 2022-03-17 01:15

from django.db import migrations


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("workspace", "0026_alter_workspaceuser_user"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="task",
            options={},
        ),
        migrations.AlterModelOptions(
            name="workspaceboardsection",
            options={},
        ),
        migrations.AlterOrderWithRespectTo(
            name="task",
            order_with_respect_to="workspace_board_section",
        ),
        migrations.AlterOrderWithRespectTo(
            name="workspaceboardsection",
            order_with_respect_to="workspace_board",
        ),
        migrations.RemoveField(
            model_name="task",
            name="order",
        ),
        migrations.RemoveField(
            model_name="workspaceboardsection",
            name="order",
        ),
    ]
