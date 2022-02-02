"""Projectify middlewares."""
from django.db import (
    transaction,
)

from .loader import (
    Loader,
)


# Graphene middlewares
def atomic_transaction_middleware(next, root, info, *args, **kwargs):
    """Wrap graphql query/mutation in transaction."""
    with transaction.atomic():
        return_value = next(root, info, *args, **kwargs)
    return return_value


def loader_middleware(next, root, info, *args, **kwargs):
    """Add loaders to info.context."""
    info.context.loader = Loader()
    return next(root, info, *args, **kwargs)
