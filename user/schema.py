"""User schema."""
from django.contrib import (
    auth,
)
from django.contrib.auth.backends import (
    ModelBackend,
)

import graphene
import graphene_django


class User(graphene_django.DjangoObjectType):
    """User."""

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
        # todo send email
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
