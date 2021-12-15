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


class Mutation(user.schema.Mutation, graphene.ObjectType):
    """Mutation object."""


schema = graphene.Schema(query=Query, mutation=Mutation)
