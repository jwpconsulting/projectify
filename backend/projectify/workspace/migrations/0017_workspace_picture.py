# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022 JWP Consulting GK
"""Add picture field to workspace."""
# Generated by Django 4.0.2 on 2022-03-02 05:52

from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("workspace", "0016_task_deadline"),
    ]

    operations = [
        migrations.AddField(
            model_name="workspace",
            name="picture",
            field=models.ImageField(
                blank=True, null=True, upload_to="workspace_picture/"
            ),
        ),
    ]
