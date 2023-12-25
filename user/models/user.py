"""User model in user app."""
from typing import (
    ClassVar,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import (
    models,
)
from django.utils import (
    crypto,
)
from django.utils.translation import gettext_lazy as _

from projectify.lib.models import BaseModel

EMAIL_CONFIRMATION_TOKEN_SALT = "email-confirmation-token-salt"
PASSWORD_RESET_TOKEN_SALT = "password-reset-token-salt"


class UserManager(BaseUserManager["User"]):
    """Manager class for User."""


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """User class."""

    email = models.EmailField(
        verbose_name=_("Email"),
        unique=True,
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
    full_name = models.CharField(
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
    objects: ClassVar[UserManager] = UserManager()

    USERNAME_FIELD = "email"

    def get_email_confirmation_token(self) -> str:
        """Return a secure email confirmation token."""
        return crypto.salted_hmac(
            key_salt=EMAIL_CONFIRMATION_TOKEN_SALT,
            value=self.email,
        ).hexdigest()

    def check_email_confirmation_token(self, token: str) -> bool:
        """Compare a hexdigest to the actual email confirmation token."""
        actual = self.get_email_confirmation_token()
        return crypto.constant_time_compare(token, actual)

    def get_password_reset_token(self) -> str:
        """Return a secure password reset token."""
        return crypto.salted_hmac(
            key_salt=PASSWORD_RESET_TOKEN_SALT,
            value=self.password,
        ).hexdigest()

    def check_password_reset_token(self, token: str) -> bool:
        """Compare a hexdigest to the actual password reset token."""
        actual = self.get_password_reset_token()
        return crypto.constant_time_compare(token, actual)
