# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023,2025 JWP Consulting GK
"""Contains enums and other constant values."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class TeamMemberRoles(models.TextChoices):
    """Roles available."""

    OBSERVER = "OBSERVER", _("Observer")
    CONTRIBUTOR = "CONTRIBUTOR", _("Contributor")
    MAINTAINER = "MAINTAINER", _("Maintainer")
    OWNER = "OWNER", _("Owner")


COLOR_MAP = {
    0: {
        "bg_class": "bg-label-orange",
        "border_class": "border-label-text-orange",
    },
    1: {
        "bg_class": "bg-label-pink",
        "border_class": "border-label-text-pink",
    },
    2: {
        "bg_class": "bg-label-blue",
        "border_class": "border-label-text-blue",
    },
    3: {
        "bg_class": "bg-label-purple",
        "border_class": "border-label-text-purple",
    },
    4: {
        "bg_class": "bg-label-yellow",
        "border_class": "border-label-text-yellow",
    },
    5: {
        "bg_class": "bg-label-red",
        "border_class": "border-label-text-red",
    },
    6: {
        "bg_class": "bg-label-green",
        "border_class": "border-label-text-green",
    },
}
