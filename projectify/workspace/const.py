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

SUBTASK_PROGRESS_CLASSES = {
    0: "w-[0%]",
    5: "w-[5%]",
    10: "w-[10%]",
    15: "w-[15%]",
    20: "w-[20%]",
    25: "w-[25%]",
    30: "w-[30%]",
    35: "w-[35%]",
    40: "w-[40%]",
    45: "w-[45%]",
    50: "w-[50%]",
    55: "w-[55%]",
    60: "w-[60%]",
    65: "w-[65%]",
    70: "w-[70%]",
    75: "w-[75%]",
    80: "w-[80%]",
    85: "w-[85%]",
    90: "w-[90%]",
    95: "w-[95%]",
    100: "w-[100%]",
}
