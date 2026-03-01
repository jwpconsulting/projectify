# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022, 2023 JWP Consulting GK
"""Ensure unique Task number for current Task objects, part two."""

from django.db import migrations


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("workspace", "0035"),
    ]

    operations = []
