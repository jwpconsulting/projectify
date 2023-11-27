"""User models."""
from typing import (
    ClassVar,
    Optional,
    cast,
)

from django.conf import (
    settings,
)
from django.contrib.auth.hashers import (
    make_password,
)
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import (
    models,
    transaction,
)
from django.utils import (
    crypto,
)
from django.utils.translation import gettext_lazy as _

from django_extensions.db.models import (
    TimeStampedModel,
)
from typing_extensions import (
    Self,
)

from .. import (
    signal_defs,
)


class UserManager(BaseUserManager["User"]):
    """Manager class for User."""

    def _create_user(
        self,
        email: str,
        password: Optional[str],
        is_staff: bool,
        is_superuser: bool,
        is_active: bool,
    ) -> "User":
        """Create and save a user with the given email, and password."""
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
        )
        user.password = make_password(password)
        user.save(using=self._db)
        user.redeem_invites()
        return user

    def create_user(
        self, email: str, password: Optional[str] = None
    ) -> "User":
        """Create a normal user."""
        return self._create_user(
            email,
            password,
            is_staff=False,
            is_superuser=False,
            is_active=False,
        )

    def create_superuser(
        self, email: str, password: Optional[str] = None
    ) -> "User":
        """Create a superuser."""
        return self._create_user(
            email,
            password,
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )


EMAIL_CONFIRMATION_TOKEN_SALT = "email-confirmation-token-salt"
PASSWORD_RESET_TOKEN_SALT = "password-reset-token-salt"


class User(AbstractBaseUser, PermissionsMixin):
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

    @transaction.atomic
    def redeem_invites(self) -> None:
        """Redeem all invites."""
        invites = UserInvite.objects.is_redeemed(False).by_email(self.email)
        for invitation in invites.iterator():
            invitation.redeem(self)


class UserInviteQuerySet(models.QuerySet["UserInvite"]):
    """User invite QuerySet."""

    def is_redeemed(self, redeemed: bool = True) -> Self:
        """Return not self redeemed invites."""
        return self.filter(redeemed=redeemed)

    def by_email(self, email: str) -> Self:
        """Filter by email."""
        return self.filter(email=email)

    @transaction.atomic()
    def invite_user(self, email: str) -> "UserInvite":
        """Invite a user."""
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise ValueError(_("User already exists."))
        invite_qs = self.by_email(email).is_redeemed(False)
        if invite_qs.exists():
            invite = invite_qs.get()
        else:
            invite = self.create(email=email)
        return invite


class UserInvite(TimeStampedModel, models.Model):
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

    def redeem(self, user: User) -> None:
        """
        Redeem this invite with a user.

        Saves.
        """
        assert not self.redeemed
        self.redeemed = True
        self.user = user
        self.save()
        signal_defs.user_invitation_redeemed.send(
            sender=self.__class__,
            user=user,
            instance=self,
        )

    objects: ClassVar[UserInviteQuerySet] = cast(  # type: ignore[assignment]
        UserInviteQuerySet, UserInviteQuerySet.as_manager()
    )
