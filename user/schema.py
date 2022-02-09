"""User schema."""
from django.contrib import (
    auth,
)

import graphene
import graphene_django

from .emails import (
    UserEmailConfirmationEmail,
    UserPasswordResetEmail,
)


class User(graphene_django.DjangoObjectType):
    """User."""

    profile_picture = graphene.String()

    def resolve_profile_picture(self, info):
        """Resolve profile_picture."""
        if self.profile_picture:
            return self.profile_picture.url

    class Meta:
        """Meta."""

        fields = ("email",)
        model = auth.get_user_model()


class SignupMutation(graphene.Mutation):
    """Signup mutation."""

    class Arguments:
        """Arguments required."""

        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(User)

    @classmethod
    def mutate(cls, root, info, email, password):
        """Mutate."""
        User = auth.get_user_model()
        user = User.objects.create_user(email=email, password=password)
        mail = UserEmailConfirmationEmail(user)
        mail.send()
        return cls(user=user)


class EmailConfirmationMutation(graphene.Mutation):
    """Mutation to confirm user email adresses for inactive users."""

    class Arguments:
        """Arguments required."""

        email = graphene.String(required=True)
        token = graphene.String(required=True)

    user = graphene.Field(User)

    @classmethod
    def mutate(cls, root, info, email, token):
        """Mutate."""
        User = auth.get_user_model()
        user = User.objects.get_by_natural_key(email)
        if user.check_email_confirmation_token(token):
            user.is_active = True
            user.save()
            return cls(user=user)


class LoginMutation(graphene.Mutation):
    """Login mutation."""

    class Arguments:
        """Arguments required."""

        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(User)

    @classmethod
    def mutate(cls, root, info, email, password):
        """Mutate."""
        from django.contrib.auth.backends import (
            ModelBackend,
        )

        user = ModelBackend().authenticate(
            info.context,
            username=email,
            password=password,
        )
        if user is None:
            return
        auth.login(
            info.context,
            user,
            backend="django.contrib.auth.backends.ModelBackend",
        )
        return cls(user=user)


class LogoutMutation(graphene.Mutation):
    """Logout mutation."""

    class Arguments:
        """No arguments required."""

    user = graphene.Field(User)

    @classmethod
    def mutate(cls, root, info):
        """Mutate."""
        user = info.context.user
        if user.is_anonymous:
            raise ValueError("User not logged in")
        auth.logout(info.context)
        return cls(user=user)


class RequestPasswordResetInput(graphene.InputObjectType):
    """RequestPasswordReset input."""

    email = graphene.String(required=True)


class RequestPasswordResetMutation(graphene.Mutation):
    """Request password reset mutation."""

    class Arguments:
        """Arguments."""

        input = RequestPasswordResetInput(required=True)

    email = graphene.String()

    @classmethod
    def mutate(cls, root, info, input):
        """Mutate."""
        User = auth.get_user_model()
        user = User.objects.get_by_natural_key(input.email)
        password_reset_email = UserPasswordResetEmail(user)
        password_reset_email.send()
        return cls(input.email)


class ConfirmPasswordResetInput(graphene.InputObjectType):
    """ConfirmPasswordReset mutation input."""

    email = graphene.String(required=True)
    token = graphene.String(required=True)
    new_password = graphene.String(required=True)


class ConfirmPasswordResetMutation(graphene.Mutation):
    """Confirm password reset."""

    class Arguments:
        """Arguments."""

        input = ConfirmPasswordResetInput(required=True)

    user = graphene.Field(User)

    @classmethod
    def mutate(cls, root, info, input):
        """Mutate."""
        User = auth.get_user_model()
        user = User.objects.get_by_natural_key(input.email)
        if user.check_password_reset_token(input.token):
            user.set_password(input.new_password)
            user.save()
            return cls(user)
        return cls(None)


class Query:
    """Query."""

    user = graphene.Field(User)

    def resolve_user(self, info):
        """Resolve user field."""
        user = info.context.user
        return user


class Mutation:
    """Mutation."""

    signup = SignupMutation.Field()
    email_confirmation = EmailConfirmationMutation.Field()
    login = LoginMutation.Field()
    logout = LogoutMutation.Field()
    request_password_reset = RequestPasswordResetMutation.Field()
    confirm_password_reset = ConfirmPasswordResetMutation.Field()
