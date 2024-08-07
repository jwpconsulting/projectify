# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Generated by Django 4.0.2 on 2022-05-27 18:50."""

import uuid

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("corporate", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="seats",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name="customer",
            name="stripe_customer_id",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="customer",
            name="subscription_status",
            field=models.CharField(
                choices=[
                    ("ACT", "Active"),
                    ("UNP", "Unpaid"),
                    ("CAN", "Canceled"),
                ],
                default="UNP",
                max_length=3,
            ),
        ),
        migrations.AddField(
            model_name="customer",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, unique=True
            ),
        ),
    ]
