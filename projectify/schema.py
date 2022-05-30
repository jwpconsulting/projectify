"""Projectify project schema."""
import strawberry

import corporate.schema
import user.schema
import workspace.schema


@strawberry.type
class Query(
    workspace.schema.Query,
    user.schema.Query,
    corporate.schema.Query,
):
    """Query object."""


@strawberry.type
class Mutation(
    workspace.schema.Mutation,
    user.schema.Mutation,
    corporate.schema.Mutation,
):
    """Mutation object."""


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)
