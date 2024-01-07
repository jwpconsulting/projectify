# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
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
"""Corporate app types."""
from typing import Literal

from django.db import models
from django.utils.translation import gettext_lazy as _

WorkspaceFeatures = Literal["full", "trial", "inactive"]


class CustomerSubscriptionStatus(models.TextChoices):
    """Customer subscription status choices."""

    # A subscription has been created with our billing provider
    ACTIVE = "ACTIVE", _("Active")
    # A subscription has never been created with our billing provider
    # TODO this should be "TRIAL" or similar
    UNPAID = "UNPAID", _("Unpaid")
    # An existing subscription with our billing provider has been cancelled
    CANCELLED = "CANCELLED", _("Cancelled")
    # A subscription does not exist, but the workspace can be used without
    # restriction
    CUSTOM = "CUSTOM", _("Custom subscription")
