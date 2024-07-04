"""Test exception_handler module."""

from typing import Literal

from django import http
from django.core import exceptions as dj_exceptions

import pytest
from rest_framework import decorators, permissions
from rest_framework import exceptions as drf_exceptions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory


@decorators.api_view()
@decorators.permission_classes([permissions.AllowAny])
def get(
    _: Request,
    code: Literal[400, 403, 404, 429],
    typ: Literal["django", "drf"],
) -> Response:
    """Produce various errors."""
    match typ, code:
        case "drf", 400:
            raise drf_exceptions.ValidationError()
        case "drf", 403:
            raise drf_exceptions.PermissionDenied()
        case "drf", 404:
            raise drf_exceptions.NotFound()
        case "drf", 429:
            raise drf_exceptions.Throttled()
        case "django", 400:
            raise dj_exceptions.ValidationError(message="Woops")
        case "django", 403:
            raise dj_exceptions.PermissionDenied()
        case "django", 404:
            raise http.Http404()
        case _:
            raise ValueError(f"Can't raise code {code} for {typ}")


@pytest.fixture
def factory() -> APIRequestFactory:
    """Create a fresh APIRequestFactory instance. A factory factory."""
    return APIRequestFactory()


def test_errors(factory: APIRequestFactory) -> None:
    """Test the various errors we can serialize."""
    request = factory.get("")
    assert get(request, 400, "drf").data == {
        "status": "invalid",
        "code": 400,
        "details": {},
        "general": "Invalid input.",
    }
    assert get(request, 403, "drf").data == {
        "status": "permission_denied",
        "code": 403,
    }
    assert get(request, 404, "drf").data == {
        "status": "not_found",
        "code": 404,
    }
    assert get(request, 429, "drf").data == {
        "status": "throttled",
        "code": 429,
    }
    assert get(request, 400, "django").data == {
        "status": "invalid",
        "code": 400,
        "details": {},
        "general": "Woops",
    }
    assert get(request, 403, "django").data == {
        "status": "permission_denied",
        "code": 403,
    }
    assert get(request, 404, "django").data == {
        "status": "not_found",
        "code": 404,
    }
