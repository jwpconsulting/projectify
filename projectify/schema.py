"""Projectify project schema."""
import strawberry
import user.schema
import workspace.schema


@strawberry.type
class Query(
    workspace.schema.Query,
    user.schema.Query,
):
    """Query object."""


@strawberry.type
class Mutation(
    workspace.schema.Mutation,
    user.schema.Mutation,
):
    """Mutation object."""


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)
