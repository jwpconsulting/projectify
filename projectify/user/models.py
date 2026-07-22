# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021-2026 JWP Consulting GK
"""User app models."""

from typing import TYPE_CHECKING, Any, ClassVar, Optional

from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from projectify.lib.models import BaseModel

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """User class."""

    email = models.EmailField(verbose_name=_("Email"), unique=True)
    unconfirmed_email = models.EmailField(
        null=True,
        blank=True,
        verbose_name=_(
            "If update email address requested, new, unconfirmed email"
        ),
    )
    # is_superuser comes from PermissionsMixin
    # is_superuser = models.BooleanField(default=False)
    # Vendor the is_staff and is_active in from AbstractUser
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."
        ),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    profile_picture = models.ImageField(
        upload_to="profile_picture/", blank=True, null=True
    )
    preferred_name = models.CharField(max_length=255, blank=True, null=True)
    activated = models.DateTimeField(
        verbose_name=_("Activated"),
        help_text=_("Date and time user account was activated"),
        editable=False,
        blank=True,
        null=True,
    )
    tos_agreed = models.DateTimeField(
        verbose_name=_("Terms of service agreed"),
        help_text=_("Date and time user has agreed to terms of service"),
        blank=True,
        null=True,
    )
    privacy_policy_agreed = models.DateTimeField(
        verbose_name=_("Privacy Policy agreed"),
        help_text=_("Date and time user has agreed to privacy policy"),
        blank=True,
        null=True,
    )
    objects: ClassVar[BaseUserManager["User"]] = BaseUserManager()

    USERNAME_FIELD = "email"

    if TYPE_CHECKING:
        userevent_set: RelatedManager["UserEvent"]

    def clean(self) -> None:
        """Validate model fields."""
        # You'd need to adjust save_user in allauth/account/adapter.py
        # without the following:
        if self.is_active and self.activated is None:
            self.activated = now()

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Override save and call full_clean."""
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Return printable user name."""
        return self.preferred_name or self.email

    def has_perm(self, perm: str, obj: Optional[object] = None) -> bool:
        """Override and ignore is_superuser."""
        result: bool = auth_models._user_has_perm(self, perm, obj)  # type: ignore
        return result

    class Meta(BaseModel.Meta):
        """Add constraints."""

        constraints = (
            models.CheckConstraint(
                name="preferred_name",
                # Match period, colon followed by space, or not period
                # or period, colon at end of word
                # type: ignore[call-arg]
                condition=models.Q(
                    preferred_name__regex=r"^([.:]\s|[^.:])*[.:]?$"
                ),
                violation_error_message=_(
                    "Preferred name can only contain '.' or ':' if followed "
                    "by whitespace or if located at the end."
                ),
            ),
        )


class UserInvite(BaseModel):
    """User invite model."""

    email = models.EmailField(verbose_name=_("Email"))
    user = models.ForeignKey[User](
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text=_("Matched user"),
    )
    redeemed = models.BooleanField(
        default=False, help_text=_("Has this invite been redeemed?")
    )
    # TODO add redeemed_when


class PreviousEmailAddress(BaseModel):
    """Store a previous email address that was associated with a user."""

    user = models.ForeignKey[User](
        User,
        on_delete=models.CASCADE,
        help_text=_("User this email address belongs to"),
    )
    email = models.EmailField(help_text=_("Previous email address"))

    def __str__(self) -> str:
        """Return email."""
        return self.email


class UserEventType(models.TextChoices):
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


class UserEvent(BaseModel):
    """Store an auditable event for user actions."""

    user = models.ForeignKey[User](User, on_delete=models.CASCADE)
    type = models.CharField(choices=UserEventType)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField()
