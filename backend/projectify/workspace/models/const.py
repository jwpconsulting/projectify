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
        "name": _("Orange"),
        "bg_class": "bg-label-orange",
        "border_class": "border-label-text-orange",
        "text_class": "text-label-text-orange",
    },
    1: {
        "name": _("Pink"),
        "bg_class": "bg-label-pink",
        "border_class": "border-label-text-pink",
        "text_class": "text-label-text-pink",
    },
    2: {
        "name": _("Blue"),
        "bg_class": "bg-label-blue",
        "border_class": "border-label-text-blue",
        "text_class": "text-label-text-blue",
    },
    3: {
        "name": _("Purple"),
        "bg_class": "bg-label-purple",
        "border_class": "border-label-text-purple",
        "text_class": "text-label-text-purple",
    },
    4: {
        "name": _("Yellow"),
        "bg_class": "bg-label-yellow",
        "border_class": "border-label-text-yellow",
        "text_class": "text-label-text-yellow",
    },
    5: {
        "name": _("Red"),
        "bg_class": "bg-label-red",
        "border_class": "border-label-text-red",
        "text_class": "text-label-text-red",
    },
    6: {
        "name": _("Green"),
        "bg_class": "bg-label-green",
        "border_class": "border-label-text-green",
        "text_class": "text-label-text-green",
    },
}
