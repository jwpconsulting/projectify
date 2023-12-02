"""Projectify project schema."""
import strawberry


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


schema = strawberry.Schema(query=Query)
