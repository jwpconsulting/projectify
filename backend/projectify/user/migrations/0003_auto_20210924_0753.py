# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021 JWP Consulting GK
"""Add permissions to users."""
# Generated by Django 3.2.7 on 2021-09-24 07:53

from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("user", "0002_auto_20210924_0747"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this user belongs to. A user will get "
                "all permissions granted to each of their groups.",
                related_name="user_set",
                related_query_name="user",
                to="auth.Group",
                verbose_name="groups",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.Permission",
                verbose_name="user permissions",
            ),
        ),
    ]
