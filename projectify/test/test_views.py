# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Test general views."""

import logging

from django.core.exceptions import BadRequest, PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.test.client import Client
from django.urls import path, reverse

import pytest
from django_ratelimit.exceptions import Ratelimited

from .. import urls


class TestHealthCheck:
    """Test health check view."""

    def test_health_check_returns_204(self, client: Client) -> None:
        """Test that health check endpoint returns 204 No Content."""
        response = client.get(reverse("health-check"))
        assert response.status_code == 204
        assert response.content == b""


@pytest.mark.django_db
class TestSitemap:
    """Test the Projectify view."""

    def test_sitemap(self, client: Client) -> None:
        """Test that the sitemap works."""
        # Not using reverse here because crawlers commonly assume
        # sitemap.xml exists. Then, the sitemap being at sitemap.xml is part
        # of the spec.
        assert client.get("/sitemap.xml").status_code == 200


def bad_request_view(request: HttpRequest) -> HttpResponse:
    """Throw a bad request error."""
    del request
    raise BadRequest("Indeed a bad request")


def forbidden_view(request: HttpRequest) -> HttpResponse:
    """Throw a generic 403 forbidden error."""
    del request
    raise PermissionDenied("Forbidden")


def ratelimited_view(request: HttpRequest) -> HttpResponse:
    """Throw a Ratelimited exception."""
    del request
    raise Ratelimited()


def csrf_protected_view(request: HttpRequest) -> HttpResponse:
    """Return OK, don't do anything else."""
    del request
    return HttpResponse("OK")


def server_error_view(request: HttpRequest) -> HttpResponse:
    """Throw a generic error and indirectly return a 500 HTTP status."""
    del request
    raise Exception("Test error")


# Combine the three error views and override the rest of the Projectify
# urlpatterns
urlpatterns = (
    path("bad-request", bad_request_view, name="bad-request"),
    path("forbidden", forbidden_view, name="forbidden"),
    path("ratelimited", ratelimited_view, name="ratelimited"),
    path("csrf-protected", csrf_protected_view, name="csrf-protected"),
    path("server-error", server_error_view, name="server-error"),
    *urls.urlpatterns,
)
# Because pytest.mark.urls override the URLconf,
# we need to manually specify these values:
handler400 = urls.handler400
handler403 = urls.handler403
handler404 = urls.handler404
handler500 = urls.handler500
csrf_failure = urls.csrf_failure


@pytest.mark.urls("projectify.test.test_views")
class Test400Error:
    """Test the 400 handler view."""

    def test_view(self, client: Client) -> None:
        """Test that we get a nice error."""
        response = client.post("/bad-request")
        assert response.status_code == 400
        assert b"Form validation failed" in response.content


@pytest.mark.urls("projectify.test.test_views")
class Test403Forbidden:
    """Test the 403 forbidden view."""

    def test_403(self, client: Client) -> None:
        """Test that a generic exception returns 403 Forbidden."""
        response = client.get("/forbidden")
        assert response.status_code == 403
        assert b"permission required to perform" in response.content

    def test_ratelimited(self, client: Client) -> None:
        """Test that a Ratelimited exception returns 429 Too Many Requests."""
        response = client.get("/ratelimited")
        assert response.status_code == 429
        assert b"making too many requests" in response.content


@pytest.mark.urls("projectify.test.test_views")
class TestCsrfFailure:
    """Test the CSRF failure view."""

    def test_csrf_view(self) -> None:
        """Test that a POST request without a CSRF token returns 403."""
        client = Client(enforce_csrf_checks=True)
        response = client.post("/csrf-protected")
        assert response.status_code == 403
        assert b"Form submission failed" in response.content

        # Visiting csrf-protected happens to already set the csrf cookie
        csrf_token = client.cookies.get("csrftoken")
        assert csrf_token, client.cookies

        data = {"csrfmiddlewaretoken": csrf_token.value}
        response = client.post("/csrf-protected", data)
        assert response.status_code == 200
        assert b"Form submission failed" not in response.content


class Test404NotFound:
    """Test the 404 not found view."""

    def test_404(
        self, client: Client, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Check log output for 404 handler."""
        with caplog.at_level(logging.WARNING):
            response = client.get("/this-page-does-not-exist/")
            assert response.status_code == 404
            assert b"Page not found" in response.content

        assert caplog.text == ""


@pytest.mark.urls("projectify.test.test_views")
class Test500InternalServerError:
    """Test the 500 internal server error view."""

    def test_500(
        self, client: Client, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test 500 status, custom template, and logging behaviour."""
        client.raise_request_exception = False
        with caplog.at_level(logging.WARNING):
            response = client.get("/server-error")
            assert response.status_code == 500
            assert b"We are sorry this happened" in response.content
        assert "Internal Server Error" in caplog.text
