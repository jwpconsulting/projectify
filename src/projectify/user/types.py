# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""User app types."""

from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class UserEventType(TextChoices):
    """Auditable user events."""

    # projectify/user/services/auth.py
    SIGN_UP = "SIGN_UP", _("sign up")
    CONFIRM_EMAIL = "CONFIRM_EMAIL", _("confirm email")
    LOG_IN = "LOG_IN", _("log in")
    LOG_OUT = "LOG_OUT", _("log out")
    REQUEST_PW_RESET = "REQUEST_PW_RESET", _("request password reset")
    CONFIRM_PW_RESET = "CONFIRM_PW_RESET", _("confirm password reset")
    # projectify/user/services/user.py
    UPDATE_PROFILE = "UPDATE_PROFILE", _("update profile")
    # This event only happens when users sign up with socialauth
    SET_PW = "SET_PW", _("set password")
    CHANGE_PW = "CHANGE_PW", _("change password")
    REQUEST_EMAIL_UPDATE = "REQUEST_EMAIL_UPDATE", _("request email update")
    CONFIRM_EMAIL_UPDATE = "CONFIRM_EMAIL_UPDATE", _("confirm email update")
    # TODO consider adding
    # Failure scenarios
    # LOG_IN_WRONG_PW = "LOG_IN_WRONG_PW", _("log in failed, wrong password")
    # LOG_IN_INACTIVE = "LOG_IN_ACTIVE", _("log in failed, inactive user")
    # REQUEST_PW_RESET_INACTIVE = (
    #     "REQUEST_PW_RESET_INACTIVE",
    #     _("request password reset failed, inactive user"),
    # )
