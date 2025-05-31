# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021-2024 JWP Consulting GK
"""User model in user app."""

from typing import Any, ClassVar

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

    class Meta(BaseModel.Meta):
        """Add constraints."""

        constraints = (
            models.CheckConstraint(
                name="preferred_name",
                # Match period, colon followed by space, or not period
                # or period, colon at end of word
                check=models.Q(
                    preferred_name__regex=r"^([.:]\s|[^.:])*[.:]?$"
                ),
                violation_error_message=_(
                    "Preferred name can only contain '.' or ':' if followed "
                    "by whitespace or if located at the end."
                ),
            ),
        )
