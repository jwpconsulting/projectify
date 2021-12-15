"""Projectify project schema."""
import graphene

import todo.schema
import user.schema
import workspace.schema


class Query(
    workspace.schema.Query,
    todo.schema.Query,
    user.schema.Query,
    graphene.ObjectType,
):
    """Query object."""


class Mutation(user.schema.Mutation, graphene.ObjectType):
    """Mutation object."""


schema = graphene.Schema(query=Query, mutation=Mutation)
