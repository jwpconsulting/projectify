"""Projectify project schema."""
import graphene
from graphene_django.debug import (
    DjangoDebug,
)

import user.schema
import workspace.schema


class Query(
    workspace.schema.Query,
    user.schema.Query,
    graphene.ObjectType,
):
    """Query object."""

    debug = graphene.Field(DjangoDebug, name="_debug")


class Mutation(
    workspace.schema.Mutation,
    user.schema.Mutation,
    graphene.ObjectType,
):
    """Mutation object."""


class Subscription(
    workspace.schema.Subscription,
    graphene.ObjectType,
):
    """Subscription object."""


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
)
