# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023,2025-2026 JWP Consulting GK
"""Contains enums and other constant values."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class TeamMemberRoles(models.TextChoices):
    """Roles available."""

    OBSERVER = "OBSERVER", _("Observer")
    CONTRIBUTOR = "CONTRIBUTOR", _("Contributor")
    MAINTAINER = "MAINTAINER", _("Maintainer")
    OWNER = "OWNER", _("Owner")


# XXX used for ProjectForm in `projectify/workspace/views/project.py`
# so it should have a more generic name
TASK_EDITOR_MIN_HEIGHT_CLASS = "min-h-[300px]"
