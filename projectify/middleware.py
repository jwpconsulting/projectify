"""Projectify middlewares."""
# https://stackoverflow.com/a/47888695
from typing import (
    Callable,
)

from django.http import (
    HttpRequest,
    HttpResponse,
)

GetResponse = Callable[[HttpRequest], HttpResponse]


class DisableCSRFMiddleware:
    """Dangerous CSRF disable middleware."""

    get_response: GetResponse

    def __init__(self, get_response: GetResponse):
        """Init."""
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Call."""
        # This is insane
        setattr(request, "_dont_enforce_csrf_checks", True)
        response = self.get_response(request)
        return response
