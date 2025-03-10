# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2022 JWP Consulting GK
"""Fix typo in enum."""
# Generated by Django 4.0.4 on 2022-06-17 08:30

from django.db import migrations, models


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
