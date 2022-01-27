"""Projectify middlewares."""
from django.db import (
    transaction,
)


# Graphene middlewares
def atomic_transaction_middleware(next, root, info, **args):
    """Wrap graphql query/mutation in transaction."""
    with transaction.atomic():
        return_value = next(root, info, **args)
    return return_value
