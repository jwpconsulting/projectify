"""User schema mutations."""
from django.contrib import (
    auth,
)

import strawberry

from ..emails import (
    UserEmailConfirmationEmail,
    UserPasswordResetEmail,
)
from . import (
    types,
)


@strawberry.input
class SignupInput:
    """Signup input."""

    email: str
    password: str


@strawberry.input
class EmailConfirmationInput:
    """EmailConfirmation input."""

    email: str
    token: str


@strawberry.input
class LoginInput:
    """Login input."""

    email: str
    password: str


@strawberry.input
class RequestPasswordResetInput:
    """RequestPasswordReset input."""

    email: str


@strawberry.input
class ConfirmPasswordResetInput:
    """ConfirmPasswordReset input."""

    email: str
    token: str
    new_password: str


@strawberry.input
class UpdateProfileInput:
    """UpdateProfile input."""

    full_name: str


@strawberry.type
class Mutation:
    """."""

    @strawberry.mutation
    def signup(self, input: SignupInput) -> types.User:
        """Mutate."""
        User = auth.get_user_model()
        user = User.objects.create_user(
            email=input.email,
            password=input.password,
        )
        mail = UserEmailConfirmationEmail(user)
        mail.send()
        return user

    @strawberry.mutation
    def email_confirmation(
        self,
        input: EmailConfirmationInput,
    ) -> types.User | None:
        """Mutate."""
        User = auth.get_user_model()
        user = User.objects.get_by_natural_key(input.email)
        if user.check_email_confirmation_token(input.token):
            user.is_active = True
            user.save()
            return user

    @strawberry.mutation
    def login(self, input: LoginInput, info) -> types.User | None:
        """Mutate."""
        from django.contrib.auth.backends import (
            ModelBackend,
        )

        user = ModelBackend().authenticate(
            info.context,
            username=input.email,
            password=input.password,
        )
        if user is None:
            return
        auth.login(
            info.context,
            user,
            backend="django.contrib.auth.backends.ModelBackend",
        )
        return user

    @strawberry.mutation
    def logout(self, info) -> types.User | None:
        """Mutate."""
        user = info.context.user
        if user.is_anonymous:
            return
        auth.logout(info.context)
        return user

    @strawberry.mutation
    def request_password_reset(self, input: RequestPasswordResetInput) -> str:
        """Mutate."""
        User = auth.get_user_model()
        user = User.objects.get_by_natural_key(input.email)
        password_reset_email = UserPasswordResetEmail(user)
        password_reset_email.send()
        return input.email

    @strawberry.mutation
    def confirm_password_reset(
        self,
        input: ConfirmPasswordResetInput,
    ) -> types.User | None:
        """Mutate."""
        User = auth.get_user_model()
        user = User.objects.get_by_natural_key(input.email)
        if user.check_password_reset_token(input.token):
            user.set_password(input.new_password)
            user.save()
            return user
        return

    @strawberry.mutation
    def update_profile(
        self,
        input: UpdateProfileInput,
        info,
    ) -> types.User | None:
        """Mutate."""
        user = info.context.user
        if not user.is_authenticated:
            return
        user.full_name = input.full_name
        user.save()
        return user
