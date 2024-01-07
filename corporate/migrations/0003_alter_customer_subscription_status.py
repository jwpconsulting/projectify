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
"""Fix typo in enum."""
# Generated by Django 4.0.4 on 2022-06-17 08:30

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        (
            "corporate",
            "0002_customer_seats_customer_stripe_customer_id_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="subscription_status",
            field=models.CharField(
                choices=[
                    ("ACT", "Active"),
                    ("UNP", "Unpaid"),
                    ("CAN", "Cancelled"),
                ],
                default="UNP",
                max_length=3,
            ),
        ),
    ]
