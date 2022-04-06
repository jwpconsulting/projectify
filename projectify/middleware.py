"""Projectify middlewares."""
from django.db import (
    transaction,
)

# from .loader import (
#     Loader,
# )


# Graphene middlewares
# def atomic_transaction_middleware(next, root, info, *args, **kwargs):
#     """Wrap graphql query/mutation in transaction."""
#     # Ensure middleware is only run once
#     if hasattr(info.context, "atomic_transaction_middleware"):
#         return next(root, info, *args, **kwargs)
#     info.context.atomic_transaction_middleware = True
#     with transaction.atomic():
#         return_value = next(root, info, *args, **kwargs)
#     return return_value
#
#
# def loader_middleware(next, root, info, *args, **kwargs):
#     """Add loaders to info.context."""
#     # Ensure middleware is only run once
#     if hasattr(info.context, "loader_middleware"):
#         return next(root, info, *args, **kwargs)
#     info.context.loader_middleware = True
#     info.context.loader = Loader()
#     return next(root, info, *args, **kwargs)


# https://stackoverflow.com/a/47888695
class DisableCSRFMiddleware:
    """Dangerous CSRF disable middleware."""

    def __init__(self, get_response):
        """Init."""
        self.get_response = get_response

    def __call__(self, request):
        """Call."""
        # This is insane
        setattr(request, "_dont_enforce_csrf_checks", True)
        response = self.get_response(request)
        return response
