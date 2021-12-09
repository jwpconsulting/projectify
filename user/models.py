from django.utils.translation import gettext_lazy as _
from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    """Manager class for User."""

    def _create_user(self, email, password, is_staff, is_superuser):
        """Create and save a user with the given email, and password."""
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None):
        """Create a normal user."""
        return self._create_user(
            email,
            password,
            is_staff=False,
            is_superuser=False,
        )

    def create_superuser(self, email, password=None):
        """Create a superuser."""
        return self._create_user(
            email,
            password,
            is_staff=True,
            is_superuser=True,
        )


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
    objects = UserManager()

    USERNAME_FIELD = "email"
