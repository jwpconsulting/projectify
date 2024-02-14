# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2021, 2023 JWP Consulting GK
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
"""Premail emails."""
from typing import (
    TYPE_CHECKING,
)

from django.contrib import (
    auth,
)

from .email import (
    TemplateEmail,
)

if TYPE_CHECKING:
    from projectify.user.models import User  # noqa: F401


class SampleEmail(TemplateEmail["User"]):
    """Sample email for testing."""

    model = auth.get_user_model()
    template_prefix = "premail/email/sample_email"
