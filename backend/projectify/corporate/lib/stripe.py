# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2024 JWP Consulting GK
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
"""Stripe related helpers."""


from stripe import StripeClient

from projectify.lib.settings import get_settings


def stripe_client() -> StripeClient:
    """Return StripeClient from CorporateConfig."""
    settings = get_settings()
    secret_key = settings.STRIPE_SECRET_KEY
    if secret_key is None:
        raise ValueError("STRIPE_SECRET_KEY is not defined")
    return StripeClient(secret_key)
