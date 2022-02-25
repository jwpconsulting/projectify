"""Authentication classes."""
from rest_framework.authentication import (
    SessionAuthentication,
)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """Custom session authentication that does not check CSRF."""

    def enforce_csrf(self, request):
        """Do not perform CSRF check."""
