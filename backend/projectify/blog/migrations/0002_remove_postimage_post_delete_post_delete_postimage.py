# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
# Generated by Django 5.0.3 on 2024-04-09 05:29
"""Clear out blog models."""

from django.db import migrations


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="postimage",
            name="post",
        ),
        migrations.DeleteModel(
            name="Post",
        ),
        migrations.DeleteModel(
            name="PostImage",
        ),
    ]
