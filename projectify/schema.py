"""Projectify project schema."""
import strawberry

import corporate.schema
import user.schema
import workspace.schema


@strawberry.type
class Query:
    """Query object."""

    @strawberry.field
    def use_drf(self) -> None:
        """
        Return nothing.

        Please migrate everything to DRF.
        """
        return None


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
