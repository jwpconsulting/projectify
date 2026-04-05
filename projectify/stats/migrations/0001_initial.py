# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Initial migration for stats app."""

from django.db import migrations, models

import projectify.lib.models


class Migration(migrations.Migration):
    """Create DailyCount model."""

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DailyCount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    projectify.lib.models.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    projectify.lib.models.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                ("name", models.CharField(max_length=2048)),
                ("date", models.DateField()),
                ("count", models.PositiveIntegerField(default=0)),
            ],
            options={
                "constraints": [
                    models.UniqueConstraint(
                        fields=["name", "date"],
                        name="unique_name_date",
                        deferrable=models.Deferrable.DEFERRED,
                    )
                ],
            },
            bases=(models.Model,),
        ),
    ]
