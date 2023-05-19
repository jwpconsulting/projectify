"""Corporate query schema."""
import uuid

import strawberry

from graphql import (
    GraphQLResolveInfo,
)

from .. import (
    models,
)
from . import (
    types,
)


@strawberry.type
class Query:
    """Query."""

    @strawberry.field
    def customerByWorkspace(
        self, info: GraphQLResolveInfo, workspace_uuid: uuid.UUID
    ) -> types.Customer:
        """Resolve customer by workspace UUID."""
        customer = models.Customer.objects.get_by_workspace_uuid(
            workspace_uuid
        )
        assert info.context.user.has_perm(
            "corporate.can_read_customer", customer
        )
        return customer  # type: ignore
