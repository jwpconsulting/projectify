"""Projectify project schema."""
import graphene

import user.schema
import workspace.schema


class Query(
    workspace.schema.Query,
    user.schema.Query,
    graphene.ObjectType,
):
    """Query object."""


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
