# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022, 2023 JWP Consulting GK
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
"""Add CUSTOM tier to subscription."""
# Generated by Django 4.2.7 on 2023-12-03 01:59

from django.db import migrations, models


class Migration(migrations.Migration):
    """Perform migration."""

    dependencies = [
        ("corporate", "0004_alter_customer_subscription_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="subscription_status",
            field=models.CharField(
                choices=[
                    ("ACTIVE", "Active"),
                    ("UNPAID", "Unpaid"),
                    ("CANCELLED", "Cancelled"),
                    ("CUSTOM", "Custom subscription"),
                ],
                default="UNPAID",
                max_length=9,
            ),
        ),
    ]
