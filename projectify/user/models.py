# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021-2026 JWP Consulting GK
"""User app models."""

from typing import Any, ClassVar, Optional

from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _

from projectify.lib.models import BaseModel


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """User class."""

    email = models.EmailField(
        verbose_name=_("Email"),
        unique=True,
    )
    unconfirmed_email = models.EmailField(
        null=True,
        blank=True,
        verbose_name=_(
            "If update email address requested, new, unconfirmed email"
        ),
    )
    is_staff = models.BooleanField()
    is_superuser = models.BooleanField()
    is_active = models.BooleanField(
        verbose_name=_("Is active"),
        default=False,
    )
    profile_picture = models.ImageField(
        upload_to="profile_picture/",
        blank=True,
        null=True,
    )
    preferred_name = models.CharField(
        max_length=255,
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

    email = models.EmailField(
        verbose_name=_("Email"),
    )
    user = models.ForeignKey[User](
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text=_("Matched user"),
    )
    redeemed = models.BooleanField(
        default=False,
        help_text=_("Has this invite been redeemed?"),
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
