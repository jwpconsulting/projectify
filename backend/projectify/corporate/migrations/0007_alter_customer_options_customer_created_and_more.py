# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
# Generated by Django 4.2.7 on 2023-12-25 05:13
"""Make Customer a BaseModel."""

import django.utils.timezone
from django.db import migrations

import projectify.lib.models


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("corporate", "0006_coupon"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customer",
            options={"get_latest_by": "modified"},
        ),
        migrations.AddField(
            model_name="customer",
            name="created",
            field=projectify.lib.models.CreationDateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="created",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="customer",
            name="modified",
            field=projectify.lib.models.ModificationDateTimeField(
                auto_now=True, verbose_name="modified"
            ),
        ),
    ]
