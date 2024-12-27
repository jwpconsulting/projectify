# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Contains enums and other constant values."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class TeamMemberRoles(models.TextChoices):
    """Roles available."""

    OBSERVER = "OBSERVER", _("Observer")
    CONTRIBUTOR = "CONTRIBUTOR", _("Contributor")
    MAINTAINER = "MAINTAINER", _("Maintainer")
    OWNER = "OWNER", _("Owner")
